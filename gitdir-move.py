#!/usr/bin/env python

import os
import sys
import subprocess

destinationParentDir = os.path.abspath(sys.argv[-1])
if not os.path.isdir(destinationParentDir):
	try:
		os.makedirs(destinationParentDir)
	except OSError:
		print 'Could not create destination directory: %s' % destinationParentDir 
		sys.exit(1)

gitFolderPaths = []
for arg in sys.argv[1:-1]:
	for root, folderNames, fileNames in os.walk(arg):
		for folderName in folderNames:
			if folderName == '.git':
				gitFolderPath = os.path.join(root, folderName)
				gitFolderPaths.append(gitFolderPath)
				print 'Found .git folder: %s' % gitFolderPath
				repoName = os.path.dirname(gitFolderPath)
				cmd = ['git', 'config', 'core.workdir', gitFolderPath]
				print cmd,
				# configReturnCode = subprocess.call(cmd)
				# if configReturnCode > 0:
				# 	print '[FAILED]'
				# 	continue
				print '[OK]'
				gitdirPath = os.path.join(destinationParentDir, repoName+'.git')
				try:
					# os.rename(gitFolderPath, gitdirPath)
					print '%s -> %s' % (gitFolderPath, gitdirPath)
				except OSError as e:
					print e.msg
					continue
				gitFileContent = 'gitdir: %s' % gitdirPath
				print '%s: "%s"' % (gitFolderPath, gitFileContent)

if len(gitFolderPaths) == 0:
	print 'No .git folders found'
	sys.exit(1)