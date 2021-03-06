
# gitdir-move
Moves all .git directories in the search path(s) to a separate location. Useful to reduce the load on synced folders etc.

## Usage:
    gitdir-move.py search_path1 [search_path2 ...] destination_parent_dir

### Example:
    gitdir-move.py /Users/bovesan/Dropbox/ /Users/bovesan/gitted/
This will move all .git directories in my Dropbox to a different folder. The .git directories will be renamed to /Users/bovesan/gitted/[repo_name].git

## How does it work?
The script is roughly equivalent to running the following commands:

    cd [repo_folder]
    git config core.workdir [repo_folder]
    mv [repo_folder]/.git [new_git_dir_path]
    echo gitdir: [new_git_dir_path] > [repo_folder]/.git

