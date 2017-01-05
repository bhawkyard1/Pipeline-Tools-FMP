export PATH=/opt/Qt5.7.0/5.7/gcc_64/bin:/opt/Qt5.7.0/Tools/QtCreator/bin:/public/bin/2016:/usr/bin:~/scripts:$PATH
#export PYTHONPATH="${PYTHONPATH}:/public/devel/2015/gaffer/lib/python2.7/lib-tk/:/opt/realflow/lib/python/lib-dynload/:/home/i7620560/tk8.6.6/unix/"
export LD_LIBRARY_PATH=$HOME/NGL/lib/:$LD_LIBRARY_PATH

COL1="\[$(tput setaf 1)\]"
COL2="\[$(tput setaf 7)\]"
RESET="\[$(tput sgr0)\]"

export PS1='\h \w $'

alias eb='gedit ~/.bashrc &'
alias edit='gedit ~/.bashrc &'

alias vs='/opt/code/bin/code -r'

alias ls='ls --color'
alias ll='ls -al'
alias bs='source ~/.bashrc'

alias c='clear'
alias r='reset'
alias p='cd ../'

alias gm='goMaya &'

alias clang11='/usr/bin/clang++ -std=c++11'

export anchdir='/home/i7620560/Documents/FMP/Pipeline-Tools-FMP'

function changeDirList()
{
	cd $1
	ls
}
alias cdl=changeDirList

function setAnchorDir()
{
	anchordir.sh
	bs
}
alias sad=setAnchorDir

function changeDirAnchor()
{
	echo 'Going to anchor directory '$anchdir
	cd $anchdir
}
alias cda=changeDirAnchor

#SDL_AUDIODRIVER=sdfsdfsdf
#export SDL_AUDIODRIVER
