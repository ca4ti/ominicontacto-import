#!/bin/bash
# Script para convertir grabaciones a mp3 pensado para correr diariamente en horas de la noche
# Modo de uso: tiene 2 argumentos que son obligatorias poner.
# Ejemplo: ./convertir.sh 1 1

Date="`which date`"
Lame="`which lame`"
Ano="`${Date} +%Y -d yesterday`"
Mes="`${Date} +%m -d yesterday`"
Dia="`${Date} +%d -d yesterday`"
Convertir=$1 # 1 si se quiere convertir a mp3 los audios, 0 si se quieren en wav
Mover_audios=$2 # 2 para mover a server remoto, 1 si se quiere mover path destino, 0 si se quiere mantener en path origen
IP=$3 # server remoto para enviar audios
Path_remoto=$4 # carpeta remota a la que se quieren pasar los audios

#Path donde estan las grabaciones en .wav, verlo en el nginx.conf, alias grabaciones
Path_origen=$ASTERISK_LOCATION/var/spool/asterisk/monitor/${Ano}-${Mes}-${Dia}
Path_destino=$ASTERISK_LOCATION/var/spool/asterisk/oml

if [ ! -d ${Path_destino} ] && [ $Mover_audios == 1 ]; then
  mkdir -p ${Path_destino}
fi

echo "Inicio: "`${Date} +%A\ %d\ "de"\ %B\ "de"\ %Y\ %T\ %Z"."`

if [ ! -d ${Path_origen} ]; then
  echo "Falló conversión, No existe el directorio de origen"
  exit 1
fi

if [ ${MONITORFORMAT} != "mp3" ]; then
  echo "Not necessary to convert files, because variable MONITORFORMAT is not mp3"
  exit 0
fi

if [ $Convertir == 0 ] && [ $Mover_audios == 0 ]; then
  echo "No se hace nada"
  echo "Fin: "`${Date} +%A\ %d\ "de"\ %B\ "de"\ %Y\ %T\ %Z"."`
  exit 1
fi

if [ $# -lt 2 ]; then
  echo "Falta uno o mas argumentos"
  echo "Usage: ./conversor.sh 1 0: convierte audios a mp3 y no cambia de ubicacion los audios"
  echo "       ./conversor.sh 0 1: no convierte audios a mp3 y cambia de ubicacion los audios a path destino"
  echo "       ./conversor.sh 1 1: convierte audios a mp3 y cambia de ubicacion los audios a path destino"
  echo "       ./conversor.sh 1 2 usuario@IP \$PATH_REMOTO: convierte audios a mp3 y cambia de ubicacion los audios a \$PATH_REMOTO en server de \$IP"
  echo "       ./conversor.sh 0 2 usuario@IP \$PATH_REMOTO: no convierte audios a mp3 y cambia de ubicacion los audios a \$PATH_REMOTO en server de \$IP"
  echo "Ingresar tercer argumento con el formato usuario@IP "
  exit 1
fi

re1="`echo "$1" | grep -E ^\-?[0-1]*\.?[0-1]+$`"
re2="`echo "$2" | grep -E ^\-?[0-2]*\.?[0-2]+$`"
if [ "$re1" == "" ] || [ "$re2" == "" ]; then
  echo "Hay alguna opción invalida, volver a correr script "
  echo "Fin: "`${Date} +%A\ %d\ "de"\ %B\ "de"\ %Y\ %T\ %Z"."`
  exit 1
fi

if [ $Convertir == 1 ]; then
  case ${CALLREC_DEVICE} in
    s3-aws)
        if [ ! -d /tmp/$Ano-$Mes-$Dia ];then
          mkdir /tmp/$Ano-$Mes-$Dia
        fi
        cd /tmp/$Ano-$Mes-$Dia
        aws s3 sync s3://${S3_BUCKET_NAME}/$Ano-$Mes-$Dia ./
        Files="`ls -ltr|awk '{print $9}'`"
        for File in ${Files};do
          if [ -f $Lame ]; then
            Sufijo="`ls ${File}|cut -d "." -f 3,3`"
            if [ $Sufijo == "mp3" ]; then
              echo -n
            else
              nice ${Lame} --quiet --preset phone $File
              ResultadoConversion=`echo $?`
              if [ ${ResultadoConversion} -ne 0 ];then
                echo "Falló al convertir el audio"
                exit 1
              else
                rm -rf $File
              fi
            fi
          fi
        done  
        aws s3 sync ./ s3://${S3_BUCKET_NAME}/$Ano-$Mes-$Dia --delete
        ResultadoCopia=`echo $?`
        if [ ${ResultadoCopia} -ne 0 ];then
              echo "Falló al copiar el audio"
              exit 1
        else
              mv ${Path_origen} /tmp/$Ano-$Mes-$Dia-$(date +"%s")
              cd .. && rm -rf ./$Ano-$Mes-$Dia
        fi
        ;;
    *)
        if [ ! -d /tmp/$Ano-$Mes-$Dia ];then
          mkdir /tmp/$Ano-$Mes-$Dia
        fi
        cd /tmp/$Ano-$Mes-$Dia
        aws http://minio:9000 --no-verify-ssl s3 sync s3://${S3_BUCKET_NAME}/$Ano-$Mes-$Dia ./
        Files="`ls -ltr|awk '{print $9}'`"
        for File in ${Files};do
          if [ -f $Lame ]; then
            Sufijo="`ls ${File}|cut -d "." -f 3,3`"
            if [ $Sufijo == "mp3" ]; then
              echo -n
            else
              nice ${Lame} --quiet --preset phone $File
              ResultadoConversion=`echo $?`
              if [ ${ResultadoConversion} -ne 0 ];then
                echo "Falló al convertir el audio"
                exit 1
              else
                rm -rf $File
              fi
            fi
          fi
        done  
        aws http://minio:9000 --no-verify-ssl s3 sync ./ s3://${S3_BUCKET_NAME}/$Ano-$Mes-$Dia --delete
        ResultadoCopia=`echo $?`
        if [ ${ResultadoCopia} -ne 0 ];then
              echo "Falló al copiar el audio"
              exit 1
        else
              mv ${Path_origen} /tmp/$Ano-$Mes-$Dia-$(date +"%s")
              cd .. && rm -rf ./$Ano-$Mes-$Dia
        fi
        ;;
  esac   
fi

echo "Se realizó el procedimiento con éxito"
echo "Fin: "`${Date} +%A\ %d\ "de"\ %B\ "de"\ %Y\ %T\ %Z"."`
