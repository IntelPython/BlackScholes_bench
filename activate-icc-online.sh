#!/bin/bash

# Install Intel Parallel Studio on Travis CI
# https://github.com/nemequ/icc-travis
#
# Originally written for Squash <https://github.com/quixdb/squash> by
# Evan Nemerson.  For documentation, bug reports, support requests,
# etc. please use <https://github.com/nemequ/icc-travis>.
#
# To the extent possible under law, the author(s) of this script have
# waived all copyright and related or neighboring rights to this work.
# See <https://creativecommons.org/publicdomain/zero/1.0/> for
# details.

( # keep variables local to this file
# Product ID, see download URL for the parts below
PRODUCT_ID=14865
PRODUCT_NAME="parallel_studio_xe_2019_update1_composer_edition_for_cpp_online"
INSTALLER_TARBALL="$PRODUCT_NAME.tgz" # can be .tar.gz or .tgz

# Default components. See ./install.sh --list_components
COMPONENTS=""

# Selectable components
COMPONENTS_TBB="intel-tbb-devel__x86_64"
COMPONENTS_MKL="intel-mkl-core-c__x86_64;intel-mkl-tbb__x86_64"
COMPONENTS_IPP="intel-ipp-mt-devel__x86_64"
COMPONENTS_ICC="intel-icc__x86_64"
COMPONENTS_DAAL="intel-daal-core__x86_64"

DESTINATION="/opt/intel"
TEMPORARY_FILES="/tmp/psxe-install"

add_components() {
    if [ ! -z "${COMPONENTS}" ]; then
        COMPONENTS="${COMPONENTS};$1"
    else
        COMPONENTS="$1"
    fi
}

while [ $# != 0 ]; do
    case "$1" in
	"--dest")
	    DESTINATION="$(realpath "$2")"; shift
	    ;;
	"--tmpdir")
	    TEMPORARY_FILES="$2"; shift
	    ;;
	"--components")
	    shift
	    OLD_IFS="${IFS}"
	    IFS=","
	    for component in $1; do
		case "$component" in
		    "icc")
			add_components "${COMPONENTS_ICC}"
		        ;;
		    "tbb")
			add_components "${COMPONENTS_TBB}"
			;;
		    "mkl")
			add_components "${COMPONENTS_MKL}"
			;;
		    "ipp")
			add_components "${COMPONENTS_IPP}"
			;;
		    "daal")
			add_components "${COMPONENTS_DAAL}"
			;;
		    *)
			echo "Unknown component '$component'"
			exit 1
			;;
		esac
	    done
	    IFS="${OLD_IFS}"
	    ;;
	*)
	    echo "Unrecognized argument '$1'"
	    exit 1
	    ;;
    esac
    shift
done

if [ -z "${COMPONENTS}" ]; then
    COMPONENTS="${COMPONENTS_ICC}"
fi

echo "Requesting components $COMPONENTS.."

INSTALLER_URL="https://registrationcenter-download.intel.com/akdlm/irc_nas/${PRODUCT_ID}/${INSTALLER_TARBALL}"
INSTALLER_TARBALL_DOWNLOAD="${TEMPORARY_FILES}/${INSTALLER_TARBALL}"
INSTALLER_DIR="${TEMPORARY_FILES}/${PRODUCT_NAME}"
INSTALLER="${INSTALLER_DIR}/install.sh"
SILENT_CFG="${INSTALLER_DIR}/silent.cfg"
SUCCESS_INDICATOR="${TEMPORARY_FILES}/icc-travis-success"

if [ ! -e "${TEMPORARY_FILES}" ]; then
    echo "${TEMPORARY_FILES} does not exist, creating..."
    mkdir -p "${TEMPORARY_FILES}" || (sudo mkdir -p "${TEMPORARY_FILES}" && sudo chown -R "${USER}:${USER}" "${TEMPORARY_FILES}")
fi

if [ ! -e "${INSTALLER_TARBALL_DOWNLOAD}" ]; then
    wget -O "${INSTALLER_TARBALL_DOWNLOAD}" "${INSTALLER_URL}" || exit 1
fi

if [ ! -e "${INSTALLER}" ]; then
    tar xvf "${INSTALLER_TARBALL_DOWNLOAD}" -C "${TEMPORARY_FILES}" || exit 1
fi
chmod u+x "${INSTALLER}"

# See https://www.intel.com/content/www/us/en/developer/articles/guide/download-documentation-intel-system-studio-current-previous.html#inpage-nav-5-3
echo "# Generated silent configuration file" > "${SILENT_CFG}"

# Accept EULA, valid values are: {accept, decline}
echo "ACCEPT_EULA=accept" >> "${SILENT_CFG}"

# Optional error behavior, valid values are: {yes, no}
echo "CONTINUE_WITH_OPTIONAL_ERROR=yes" >> "${SILENT_CFG}"

# Install location, valid values are: {/opt/intel, filepat=the file location pattern (/file/location/to/license.lic)}
echo "PSET_INSTALL_DIR=${DESTINATION}" >> "${SILENT_CFG}"

# Continue with overwrite of existing installation directory, valid values are: {yes, no}
echo "CONTINUE_WITH_INSTALLDIR_OVERWRITE=yes" >> "${SILENT_CFG}"

# List of components to install (use semicolon to separate the components), valid values are: {ALL, DEFAULTS, comppat}
echo "COMPONENTS=${COMPONENTS}" >> "${SILENT_CFG}"

# Installation mode, valid values are: {install, repair, uninstall}
echo "PSET_MODE=install" >> "${SILENT_CFG}"

# Activation type, valid values are: {exist_lic, license_server, license_file, serial_number}
echo "ACTIVATION_TYPE=serial_number" >> "${SILENT_CFG}"

# Serial number, valid values are: {snpat}
# ENCRYPT BEFORE TRYING ON TRAVIS!!!
if [ "x" != "x${INTEL_SERIAL_NUMBER}" ]; then
    echo "ACTIVATION_SERIAL_NUMBER=${INTEL_SERIAL_NUMBER}" >> "${SILENT_CFG}"
else
    echo "Missing serial number. travis encrypt INTEL_SERIAL_NUMBER=XXXX-XXXXXXX"
    echo "Warning! This script is for automation purposes only. It installs globally and modifies .bashrc"
    exit 1
fi

# Intel(R) Software Improvement Program
#
# To improve our software and customer experience, Intel would like to collect technical
# information about your software installation and runtime status (such as installation metrics,
# license/support types, software SKU/serial, counters, flags, and timestamps)
# and development environment (such as operating system, CPU architecture,
# last 4-digits of the MAC address and other Intel products installed). ("Information").
#
# Information collected under this notice may be retained by Intel indefinitely but
# it will not be shared outside of Intel or its wholly-owned subsidiaries.
#
# You can revoke your consent at any time by choosing "Improvement Program Options" in the "Settings" tab of
# the Intel(R) Software Manager and selecting the "I do NOT consent to the collection of my Information" option.
# For more details please refer to this article:
# https://www.intel.com/content/www/us/en/developer/articles/community/software-improvement-program.html
#
# Yes - I consent to the collection of my Information
# No  - I do NOT consent to the collection of my Information
#, valid values are: {yes, no}
echo "INTEL_SW_IMPROVEMENT_PROGRAM_CONSENT=no" >> "${SILENT_CFG}"

# Enable check for updates mode, valid values are: {yes, no}
#echo "CHECK_FOR_UPDATES_MODE=no" >> "${SILENT_CFG}"

# Enable Android* NDK integration, valid values are: {yes, no}
#echo "NDK_INTEGRATION_ENABLED=no" >> "${SILENT_CFG}"

# Enable Wind River* Linux Build Environment Integration, valid values are: {yes, no}
#echo "WB_INTEGRATION_ENABLED=no" >> "${SILENT_CFG}"

attempt=1;
while [ $attempt -le 3 ]; do
    # if [ ! -e "${TEMPORARY_FILES}/parallel-studio-install-data" ]; then
    # 	mkdir -p "${TEMPORARY_FILES}/parallel-studio-install-data" || (sudo mkdir -p "${TEMPORARY_FILES}/parallel-studio-install-data" && sudo chown -R "${USER}:${USER}" "${TEMPORARY_FILES}")
    # fi

    ("${INSTALLER}" -s "${SILENT_CFG}" && \
        touch "${SUCCESS_INDICATOR}") &

    # So Travis doesn't die in case of a long download/installation.
    #
    # NOTE: a watched script never terminates.
    elapsed=0;
    while kill -0 $! 2>/dev/null; do
        sleep 1
        elapsed=$(expr $elapsed + 1)
        if [ $(expr $elapsed % 60) -eq 0 ]; then
            mins_elapsed=$(expr $elapsed / 60)
            if [ $mins_elapsed = 1 ]; then
                minute_string="minute"
            else
                minute_string="minutes"
            fi
            echo "Still running... (about $(expr $elapsed / 60) ${minute_string} so far)."
        fi
    done

    if [ ! -e "${SUCCESS_INDICATOR}" ]; then
        echo "Installation failed."
        exit 1
    fi

    if [ ! -e "${DESTINATION}/bin/compilervars.sh" ]; then
        # Sometimes the installer returns successfully without actually
        # installing anything.  Let's try again…
        echo "Installation attempt #${attempt} completed, but unable to find compilervars.sh."
        find "${DESTINATION}"
    else
        break
    fi

    echo "Trying again..."

    attempt=$(expr $attempt + 1)
done

if [ ! -e "${DESTINATION}/bin/compilervars.sh" ]; then
    echo "Installation failed."
    exit 1
fi

# Add configuration information to ~/.bashrc.  Unfortunately this will
# not be picked up automatically by Travis, so you'll still need to
# source ~/.bashrc in your .travis.yml
echo "export INTEL_INSTALL_PATH=\"${DESTINATION}\"" > ~/.bashrc-intel
echo ". \"\${INTEL_INSTALL_PATH}/bin/compilervars.sh\" intel64" >> ~/.bashrc-intel
echo "export LD_LIBRARY_PATH=\"\${INTEL_INSTALL_PATH}/lib/intel64:\$LD_LIBRARY_PATH\"" >> ~/.bashrc-intel
echo "export PATH=\"\${INTEL_INSTALL_PATH}/bin:\$PATH\"" >> ~/.bashrc-intel
echo ". ~/.bashrc-intel" >> ~/.bashrc
) # end of local scope
. ~/.bashrc-intel
