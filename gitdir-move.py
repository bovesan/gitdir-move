#!/usr/bin/env python

import os
import sys
import subprocess
import shutil

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
	for root, folderNames, fileNames in os.walk(os.path.abspath(arg)):
		for folderName in folderNames:
			if folderName == '.git':
				gitFolderPath = os.path.join(root, folderName)
				gitFolderPaths.append(gitFolderPath)
				os.chdir(gitFolderPath)
				# print 'Found .git folder: %s' % gitFolderPath
				repoName = os.path.basename(os.path.dirname(gitFolderPath))
				try:
					cmd = ['git', 'config', 'remote.origin.url']
					gitRemoteUrl = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].splitlines()[0]
					if '/' in gitRemoteUrl:
						repoName = os.path.basename(gitRemoteUrl)
				except IndexError:
					pass
				while repoName.endswith('.git'):
					repoName = repoName[:-4]
				cmd = ['git', 'config', 'core.workdir', gitFolderPath]
				# print cmd,
				configReturnCode = subprocess.call(cmd)
				if configReturnCode > 0:
					print cmd, '[FAILED]'
					continue
				# print cmd, '[OK]'
				gitdirPath = os.path.join(destinationParentDir, repoName+'.git')
				i = 0
				while os.path.exists(gitdirPath):
					i += 1
					repoNameResolved = repoName + '.%i' % i
					gitdirPath = os.path.join(destinationParentDir, repoNameResolved+'.git')
					# print 'Cannot move %s Destination already exist: %s' % (gitFolderPath, gitdirPath)
					# continue
				try:
					shutil.move(gitFolderPath, gitdirPath)
					print '%s -> %s' % (gitFolderPath, gitdirPath)
				except OSError as e:
					print 'Could not move %s -> %s' % (gitFolderPath, gitdirPath),
					print e.strerror
					continue
				gitFileContent = 'gitdir: %s' % gitdirPath
				try:
					open(gitFolderPath, 'w').write(gitFileContent)
				except IOError as e:
					print '  Error: Could not write to .git file. Rolling back:'
					try:
						shutil.move(gitdirPath, gitFolderPath)
						print '  %s -> %s' % (gitFolderPath, gitdirPath)
					except OSError as e:
						print e.strerror
						continue
				# print '%s: "%s"' % (gitFolderPath, gitFileContent)

if len(gitFolderPaths) == 0:
	print 'No .git folders found in %s' % sys.argv[1:-1]
	sys.exit(1)
