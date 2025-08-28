# coding=utf8
# ***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
# **************************************************************************************/

import os
import re
import subprocess
import tarfile
from glob import iglob

import requests

from ..logger import warning, debug

__all__ = ["use_rtl", "download_rtl"]


def use_rtl(rtl_file: str, out_dir: str) -> None:
    """Extracts an RTL tarball and creates a symbolic link to its contents.

    If the tarball is not already extracted, this function extracts it into a
    directory named after the tarball. It then creates a symlink named 'rtl'
    in the output directory, pointing to the 'rtl' subdirectory within the
    extracted folder. Any existing 'rtl' symlink is removed first.

    Args:
        rtl_file (str): The filename of the RTL tarball (e.g., 'openxiangshan-kmh-abc114514-1919810.tar.gz').
        out_dir (str): The directory where the tarball is located and where the
            symlink will be created.
    """
    rtl_path = os.path.join(out_dir, rtl_file)
    dir_name = os.path.basename(rtl_file).replace(".tar.gz", "")
    rtl_dir = os.path.join(out_dir, dir_name)
    if not os.path.exists(rtl_dir):
        debug("Extract %s to %s" % (rtl_path, out_dir))
        with tarfile.open(rtl_path, "r:gz") as tar:
            tar.extractall(path=rtl_dir)
    lnk_file = os.path.join(out_dir, "rtl")
    if os.path.exists(lnk_file):
        debug("Remove old link %s" % lnk_file)
        os.remove(lnk_file)
    os.symlink(os.path.join(rtl_dir, "rtl"), lnk_file)


def wget(url: str, out_dir: str) -> int:
    """Downloads a file from a URL using wget.
    Args:
        url (str): The URL to download the file from.
        out_dir (str): The directory where the file is located.

    Returns:
        int: The return code of `wget`
    """
    ret = subprocess.run(["wget", url, "-P", out_dir])
    return ret.returncode


def download_rtl(base_url: str, out_dir: str, version="latest") -> bool:
    """Downloads and sets up a specific version of an RTL.

    Checks for a local copy of the specified RTL version first. If not found,
    it downloads the tarball from the `base_url`. The URL can be a direct link
    to a .tar.gz file or a webpage containing such links. If a version is
    specified, it attempts to find a matching file; otherwise, it defaults to
    the first available link. After downloading, it calls `use_rtl` to extract
    the archive and create a symlink.

    Args:
        base_url (str): The URL to download the RTL from.
        out_dir (str): The directory to save the downloaded file.
        version (str): The version of the RTL to download. Defaults to "latest".

    Returns:
        bool: True if the RTL is successfully downloaded and set up.
    """
    debug("Download RTL from %s (%s)", base_url, version)
    rtl_pattern = f"{out_dir}/*.tar.gz"
    if version != "latest":
        for f in iglob(rtl_pattern):
            if version in f:
                debug("find %s in %s, ignore download" % (f, out_dir))
                use_rtl(f, out_dir)
                return True
        if version in base_url and ".tar.gz" in base_url:
            wget(base_url, out_dir)
        for f in iglob(rtl_pattern):
            if version in f:
                debug("download %s success" % f)
                use_rtl(f, out_dir)
                return True
    if not base_url.endswith(".tar.gz"):
        resp = requests.get(base_url).content.decode('utf-8')
        all_keys = []
        all_urls = {}
        url = None
        for u in re.findall(r'http[s]?://\S+?\.tar\.gz', resp):
            key = u.split("/")[-1].strip()
            all_keys.append(key)
            all_urls[key] = u
            if version and version in u:
                url = u
                break
        if url is None:
            if version:
                warning(f"version {version} not found in {all_urls.keys()}, download the first one")
            assert len(all_urls) > 0, "No download url found (resp: %s)" % resp
            file_to_download = all_keys[0]  # find the latest version
            for f in iglob(rtl_pattern):
                if file_to_download in f:
                    debug("find %s in %s, ignore download", f, out_dir)
                    use_rtl(f, out_dir)
                    return True
            url = all_urls[file_to_download]
        debug(f"download {url} to {out_dir}")
        assert wget(url, out_dir) == 0, "Download RTL failed"
        use_rtl(url.split("/")[-1], out_dir)
    else:
        assert wget(base_url, out_dir) == 0, "Download RTL failed"
        use_rtl(base_url.split("/")[-1], out_dir)
    return True
