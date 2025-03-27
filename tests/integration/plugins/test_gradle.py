# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2025 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import textwrap
from pathlib import Path

import pytest
import yaml

from craft_parts import LifecycleManager, Step

# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2023 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


@pytest.fixture
def local_proxy_url():
    conf_file = Path("proxy.conf")
    conf_file.write_text(
        """
Port 8888
Timeout 600
DefaultErrorFile "/usr/share/tinyproxy/default.html"
StatFile "/usr/share/tinyproxy/stats.html"
LogFile "/var/log/tinyproxy/tinyproxy.log"
LogLevel Info
PidFile "/run/tinyproxy/tinyproxy.pid"
MaxClients 100
Allow 127.0.0.1
Allow ::1
ViaProxyName "tinyproxy"
    """,
        encoding="utf-8",
    )
    proc = subprocess.Popen(["sudo", "tinyproxy", "-d", str(conf_file)])
    yield "http://localhost:8888"
    proc.kill()


def test_gradle_plugin_gradlew(new_dir, monkeypatch, partitions, local_proxy_url):
    source_location = Path(__file__).parent / "test_gradle"
    monkeypatch.chdir(source_location)
    monkeypatch.setenv("http_proxy", local_proxy_url)
    monkeypatch.setenv("https_proxy", local_proxy_url)
    monkeypatch.setenv("GRADLE_USER_HOME", f"{new_dir}/parts/foo/build/.gradle")
    parts_yaml = textwrap.dedent(
        f"""
        parts:
          foo:
            plugin: gradle
            gradle-task: build
            gradle-init-script: init.gradle
            gradle-init-script-parameters: [testWrite]
            source: {source_location}
            build-packages: [gradle, default-jdk]
            stage-packages: [default-jre-headless]
        """
    )
    parts = yaml.safe_load(parts_yaml)

    lf = _execute_plugin(parts=parts, new_dir=new_dir, partitions=partitions)
    prime_dir = lf.project_info.prime_dir
    java_binary = Path(prime_dir, "bin", "java")
    assert java_binary.is_file()

    output = subprocess.check_output(
        [str(java_binary), "-jar", f"{prime_dir}/jar/HelloWorld-1.0.jar"], text=True
    )
    assert output.strip() == "Hello from Gradle-built Java"


def _execute_plugin(parts, new_dir, partitions) -> LifecycleManager:
    lf = LifecycleManager(
        parts,
        application_name="test_ant",
        cache_dir=new_dir,
        work_dir=new_dir,
        partitions=partitions,
    )
    actions = lf.plan(Step.PRIME)

    with lf.action_executor() as ctx:
        ctx.execute(actions)

    return lf


def test_gradlew_plugin_gradle(new_dir, monkeypatch, partitions):
    source_location = Path(__file__).parent / "test_gradle"
    monkeypatch.chdir(source_location)
    monkeypatch.setenv("http_proxy", "abc")
    monkeypatch.setenv("https_proxy", "def")
    monkeypatch.setenv("no_proxy", "localhost")
    parts_yaml = textwrap.dedent(
        f"""
        parts:
          foo:
            plugin: gradle
            gradle-task: build
            source: {source_location}
            build-packages: [gradle, default-jdk]
            stage-packages: [default-jre-headless]
        """
    )
    parts = yaml.safe_load(parts_yaml)
    (source_location / "gradlew").unlink(missing_ok=True)

    lf = _execute_plugin(parts=parts, new_dir=new_dir, partitions=partitions)

    prime_dir = lf.project_info.prime_dir
    java_binary = Path(prime_dir, "bin", "java")
    assert java_binary.is_file()

    output = subprocess.check_output(
        [str(java_binary), "-jar", f"{prime_dir}/jar/HelloWorld-1.0.jar"], text=True
    )
    assert output.strip() == "Hello from Gradle-built Java"
