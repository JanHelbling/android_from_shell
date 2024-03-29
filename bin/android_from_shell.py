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

import os,sys,argparse,configparser

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
		os.mkdir('{}/lib'.format(NAME))
		os.mkdir('{}/bin'.format(NAME))
		os.mkdir('{}/res'.format(NAME))
		os.mkdir('{}/res/layout'.format(NAME))
		os.mkdir('{}/res/values'.format(NAME))
		os.mkdir('{}/res/drawable'.format(NAME))
	
	def write_files(self):
		with open('{}/src/{}/{}/{}/MainActivity.java'.format(NAME,P1,P2,P3),'w') as fd:
			fd.write("package "+P1+"."+P2+"."+P3+""";
import android.app.*;
import android.os.*;

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
    android:minSdkVersion="28"
    android:targetSdkVersion="28" />
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
		self.aapt_3()
		print("Now Sign the APK!")
		if not os.path.exists("../mykey.keystore"):
			print("EXECUTE: keytool -genkeypair -validity 365 -keystore mykey.keystore -keyalg RSA -keysize 2048")
			print("EXECUTE: {}/zipalign -f 4 ./{}/bin/app.unaligned.apk app.apk".format(BT,NAME))
			print("EXECUTE: {}/apksigner sign --ks mykey.keystore app.apk".format(BT))
		else:
			self.zipalign_4()
			print("Enter keystore-password:")
			print(os.getcwd())
			os.system("{}/apksigner sign --ks ../mykey.keystore ../app.apk".format(BT))
			print("DONE! app.apk created!")
	def aapt_1(self):
		os.system('{}/aapt package -f -m -J ./src -M ./AndroidManifest.xml -S ./res -I {}/android.jar'.format(BT,PF))
	
	def aapt_2(self):
		os.system('{}/aapt package -f -m -F ./bin/app.unaligned.apk -M ./AndroidManifest.xml -S ./res -I {}/android.jar'.format(BT,PF))
	
	def javac(self):
		os.system('javac -d obj -classpath "{}/android.jar" src/{}/{}/{}/*.java'.format(PF,P1,P2,P3))
	
	def dx(self):
		os.system('{}/d8 ./obj/{}/{}/{}/*'.format(BT,P1,P2,P3))
	
	def aapt_3(self):
		os.system('{}/aapt add ./bin/app.unaligned.apk classes.dex'.format(BT))
	
	def zipalign_4(self):
		os.system("{}/zipalign -f 4 ../{}/bin/app.unaligned.apk ../app.apk".format(BT,NAME))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='android_from_shell.py'
	)
	parser.add_argument(
		'create|build'
	)
	parser.add_argument(
		'--package-name','-p', default="com.example.hello", type=str,
		help='packagename, with two points \'.\' eg. com.example.hello',dest='pname')
	parser.add_argument(
		'--app-name','-a',default='Hello',type=str,
		help='appname, eg. Hello',dest='aname')
	args = parser.parse_args()
	NAME		=	args.aname
	PACKAGENAME	=	args.pname
	config = configparser.ConfigParser()
	if NAME + PACKAGENAME == 'Hellocom.example.hello' and os.path.exists('.android_from_shell.cfg'):
		config.read('.android_from_shell.cfg')
		NAME		= config['Application']['ANAME']
		PACKAGENAME	= config['Application']['PNAME']
	else:
		config["Application"] = {'ANAME': NAME,'PNAME': PACKAGENAME}
		with open('.android_from_shell.cfg', 'w') as configfile:
			config.write(configfile)
	print("NAME: ",NAME)
	print("PNAME:",PACKAGENAME)
	P1		=	PACKAGENAME.split(".")[0]
	P2		=	PACKAGENAME.split(".")[1]
	P3		=	PACKAGENAME.split(".")[2]
	if 'create' == sys.argv[1]:
		a = create_files()
	elif 'build' == sys.argv[1]:
		a = build()
