# test if we are in the project
localdir=${PWD##*/}
if [ ${localdir=} = "NAO-Map-UV30-2018" ]; then
  echo "ok"
  #RemotePath=/home/newubu/MyApps/Nao/v-rep/nao-new-model/build/
  RemotePath=/public/share/uv27spid/
  ReleaseDate="20180402"
  ExternalLibNaoqiGz=naoqi-${ReleaseDate}.tgz
  ExternalLibPynaoqiGz=pynaoqi-${ReleaseDate}.tgz
  ExternalLibVrepGz=v-rep-${ReleaseDate}.tgz
  tar xvfz ${RemotePath}${ExternalLibNaoqiGz}
  tar xvfz ${RemotePath}${ExternalLibPynaoqiGz}
  tar xvfz ${RemotePath}${ExternalLibVrepGz}
else
  echo "not in NAO-Map-UV30-2018, try again"
fi



