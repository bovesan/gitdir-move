#!/usr/bin/env python

import os
import sys
import subprocess

usage = 'Usage: gitdir-move.py search_path1 [search_path2 ...] destination_parent_dir'

if len(sys.argv) < 3:
	print usage
	sys.exit(1)

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
				gitFolderPath = os.path.abspath(os.path.join(root, folderName))
				gitFolderPaths.append(gitFolderPath)
				# print 'Found .git folder: %s' % gitFolderPath
				repoName = os.path.basename(os.path.dirname(gitFolderPath))
				cmd = ['git', 'config', 'core.workdir', gitFolderPath]
				# print cmd,
				configReturnCode = subprocess.call(cmd)
				if configReturnCode > 0:
					print cmd, '[FAILED]'
					continue
				# print cmd, '[OK]'
				gitdirPath = os.path.join(destinationParentDir, repoName+'.git')
				try:
					os.rename(gitFolderPath, gitdirPath)
					print '%s -> %s' % (gitFolderPath, gitdirPath)
				except OSError as e:
					print e.strerror
					continue
				gitFileContent = 'gitdir: %s' % gitdirPath
				try:
					open(gitFolderPath, 'w').write(gitFileContent)
				except IOError as e:
					print '  Error: Could not write to .git file. Rolling back:'
					try:
						os.rename(gitdirPath, gitFolderPath)
						print '  %s -> %s' % (gitFolderPath, gitdirPath)
					except OSError as e:
						print e.strerror
						continue
				# print '%s: "%s"' % (gitFolderPath, gitFileContent)

if len(gitFolderPaths) == 0:
	print 'No .git folders found in %s' % sys.argv[1:-1]
	sys.exit(1)
	