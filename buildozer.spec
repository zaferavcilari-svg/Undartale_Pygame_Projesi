[app]

# (str) Title of your application
title = undertale projesi

# (str) Package name
package.name = undertaleprojesi

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yildirim123

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements
requirements = python3,kivy,pygame

# (str) Name of the Python file with the application entrypoint (usually main.py)
main.py = undertale.py

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,ogg,mp3,ttf

# (str) Application versioning (method 1)
version = 0.1

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# 🛑 NDK yolunu manuel zorlama (Çözüm 1)
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (list) Permissions
android.permissions = android.permission.INTERNET, android.permission.READ_EXTERNAL_STORAGE, android.permission.WRITE_EXTERNAL_STORAGE


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
