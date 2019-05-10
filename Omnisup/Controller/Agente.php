<?php
/* Copyright (C) 2018 Freetech Solutions

 This file is part of OMniLeads

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see http://www.gnu.org/licenses/.

*/
include $_SERVER['DOCUMENT_ROOT'] . '/Omnisup/config.php';
include entities. '/QueueMember.php';
include models . '/Agente_Model.php';

class Agente {

    private $Agente_Model;
    private $keyWords;

    function __construct() {
        $this->keyWords = array('Host', 'Dyn', 'Forcerport', 'Comedia', 'ACL', 'Port');
        $this->Agente_Model = new Agente_Model();
    }

    function traerAgentes($campName) {
        $result = $this->Agente_Model->getAgents($campName);
        $arrClaves = $arrUsername = $arrUserId = $arrGrupoId = array();
        foreach ($result as $clave => $valor) {
            if(is_array($valor)) {
                foreach ($valor as $key => $value) {
                    if ($key == "id") {
                        $arrClaves[] = $value;
                    }
                    if ($key == "username") {
                        $arrUsername[] = $value;
                    }
                    if ($key == "grupo_id") {
                        $arrGrupoId[] = $value;
                    }
                    if ($key == "user_id") {
                        $arrUserId[] = $value;
                    }
                }
            }
        }
        $arrResult['ids'] = $arrClaves;
        $arrResult['nombres_usuario'] = $arrUsername;
        $arrResult['ids_grupo'] = $arrGrupoId;
        $arrResult['ids_user'] = $arrUserId;
        return $arrResult;
    }


    function traerEstadoAgente($idAgent) {
        $statusResult = $this->Agente_Model->getAgentStatus($idAgent);
      	$rawArrayData = array();
      	foreach($statusResult as $clave => $valor) {
      	    $Qm = new QueueMember();
      	    $valor = explode(":", $valor);//settear nombre y extension
      	    $Qm->setStatus($valor[0]);
            $Qm->setTime($valor[1]);
            $Qm->setId($idAgent);
      	    $rawArrayData[] = $Qm;
      	}
        return $rawArrayData;
    }

    function traerTipoPausa($agent) {
        $data = $this->Agente_Model->getPauseAgents($agent);
        foreach ($data as $clave => $valor) {
            if ($clave == 'data') {
                $arrData = explode(":", $valor);
            }
        }
        return $arrData;
    }

    function ejecutarAccion($agt, $ext, $accion) {//"AGENTLOGOUT"/"AGENTUNPAUSE"/"AGENTPAUSE"/"CHANTAKECALL"/"CHANSPYWISHPER"/"CHANSPY"/"CHANCONFER"
        $res = $this->Agente_Model->ExecAction($agt, $ext, $accion);
        return $res;
    }

}