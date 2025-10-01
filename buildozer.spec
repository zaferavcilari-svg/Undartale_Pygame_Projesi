[app]
title = undertale projesi
package.name = undertaleprojesi
package.domain = com.yildirim123
source.dir = .
requirements = python3,kivy,pygame
main.py = undertale.py
source.include_exts = py,png,jpg,kv,atlas,wav,ogg,mp3,ttf
version = 0.1
orientation = portrait
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.permissions = android.permission.INTERNET, android.permission.READ_EXTERNAL_STORAGE, android.permission.WRITE_EXTERNAL_STORAGE
[buildozer]
log_level = 2
bin_dir = ./bin
