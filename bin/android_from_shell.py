#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    android_from_shell.py
#    A commandline-tool to create Android-Apps without GUI
#
#    Copyright (C) 2020 by Jan Helbling <jh@jan-helbling.ch>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os,sys

BT	=	os.getenv('BUILD_TOOLS')
PF	=	os.getenv('APLATFORM')
if BT == None:
	print('$BUILD_TOOLS not set! you need it!')
	print('Example: export BUILD_TOOLS=/opt/android-sdk/build-tools/26.0.1/')
	exit(1)
if PF == None:
	print('$APLATFORM not set! you need it!')
	print('Example: export APLATFORM=/opt/android-sdk/platforms/android-19/')
	exit(1)

NAME		=	"HelloAndroid"
PACKAGENAME	=	"com.example.hello"
P1		=	"com"
P2		=	"example"
P3		=	"hello"

class create_files:
	def __init__(self):
		self.create_folders()
		self.write_files()
	
	def create_folders(self):
		os.mkdir('{}'.format(NAME))
		os.mkdir('{}/src/'.format(NAME))
		os.mkdir('{}/src/{}'.format(NAME,P1))
		os.mkdir('{}/src/{}/{}'.format(NAME,P1,P2))
		os.mkdir('{}/src/{}/{}/{}'.format(NAME,P1,P2,P3))
		os.mkdir('{}/obj'.format(NAME))
		os.mkdir('{}/bin'.format(NAME))
		os.mkdir('{}/res'.format(NAME))
		os.mkdir('{}/res/layout'.format(NAME))
		os.mkdir('{}/res/values'.format(NAME))
		os.mkdir('{}/res/drawable'.format(NAME))
	
	def write_files(self):
		with open('{}/src/{}/{}/{}/MainActivity.java'.format(NAME,P1,P2,P3),'w') as fd:
			fd.write("package "+P1+"."+P2+"."+P3+""";
import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {
   @Override
   protected void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      setContentView(R.layout.activity_main);
   }
}""")
		with open('{}/res/values/strings.xml'.format(NAME),'w') as fd:
			fd.write("""<resources>
   <string name="app_name">A Hello Android</string>
   <string name="hello_msg">Hello Android!</string>
   <string name="menu_settings">Settings</string>
   <string name="title_activity_main">MainActivity</string>
</resources>""")
		
		with open('{}/AndroidManifest.xml'.format(NAME),'w') as fd:
			fd.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest
  xmlns:android=
    "http://schemas.android.com/apk/res/android"
  package="{}.{}.{}"
  android:versionCode="1"
  android:versionName="1.0" >
  <uses-sdk
    android:minSdkVersion="29"
    android:targetSdkVersion="29" />
  <application
    android:allowBackup="true"
    android:label="@string/app_name" >
    <activity
      android:name=
        ".MainActivity"
      android:label="@string/app_name" >
      <intent-filter>
        <action android:name=
          "android.intent.action.MAIN" />
        <category android:name=
          "android.intent.category.LAUNCHER" />
      </intent-filter>
    </activity>
  </application>
</manifest>""".format(P1,P2,P3))
		
		with open('{}/res/layout/activity_main.xml'.format(NAME),'w') as fd:
			fd.write("""<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools"
   android:layout_width="match_parent"
   android:layout_height="match_parent" >
   
   <TextView
      android:layout_width="wrap_content"
      android:layout_height="wrap_content"
      android:layout_centerHorizontal="true"
      android:layout_centerVertical="true"
      android:text="@string/hello_msg"
      tools:context=".MainActivity" />
</RelativeLayout>""")

class build:
	def __init__(self):
		os.chdir("{}".format(NAME))
		self.aapt_1()
		self.javac()
		self.dx()
		self.aapt_2()
		self.cp()
		self.aapt_3()
		print("Now Sign the APK!")
		if not os.path.exists("../mykey.keystore"):
			print("EXECUTE: keytool -genkeypair -validity 365 -keystore mykey.keystore -keyalg RSA -keysize 2048")
			print("EXECUTE: {}/apksigner sign --ks mykey.keystore ./{}/bin/app.unaligned.apk".format(BT,NAME))
			print("EXECUTE: {}/zipalign -f 4 ./{}/bin/app.unaligned.apk app.apk".format(BT,NAME))
		else:
			print("Enter keystore-password:")
			os.system("{}/apksigner sign --ks ../mykey.keystore ./bin/app.unaligned.apk".format(BT))
			self.zipalign_4()
			print("DONE! app.apk created!")
	def aapt_1(self):
		os.system('{}/aapt package -f -m -J ./src -M ./AndroidManifest.xml -S ./res -I {}/android.jar'.format(BT,PF))
	
	def aapt_2(self):
		os.system('{}/aapt package -f -m -F ./bin/app.unaligned.apk -M ./AndroidManifest.xml -S ./res -I {}/android.jar'.format(BT,PF))
	
	def javac(self):
		os.system('javac -d obj -classpath src -bootclasspath {}/android.jar src/{}/{}/{}/*.java'.format(PF,P1,P2,P3))
	
	def dx(self):
		os.system('{}/dx --dex --output=./bin/classes.dex ./obj'.format(BT))
	
	def cp(self):
		os.system('cp ./bin/classes.dex .')
	
	def aapt_3(self):
		os.system('{}/aapt add ./bin/app.unaligned.apk classes.dex'.format(BT))
	
	def zipalign_4(self):
		os.system("{}/zipalign -f 4 ../{}/bin/app.unaligned.apk ../hello.apk".format(BT,NAME))

if __name__ == '__main__':
	if sys.argv.__len__() not in  [4,2]:
		print("Usage: {} <create|build> NAME PACKAGENAME".format(sys.argv[0]))
		exit(1)
	NAME		=	sys.argv[2]
	PACKAGENAME	=	sys.argv[3]
	P1		=	PACKAGENAME.split(".")[0]
	P2		=	PACKAGENAME.split(".")[1]
	P3		=	PACKAGENAME.split(".")[2]
	if 'create' == sys.argv[1]:
		a = create_files()
	elif 'build' == sys.argv[1]:
		a = build()
