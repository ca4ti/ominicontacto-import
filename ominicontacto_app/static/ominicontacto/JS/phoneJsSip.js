//***************************************************
var lastDialedNumber, entrante, config, textSipStatus, callSipStatus, iconStatus, userAgent, sesion, opciones, eventHandlers, flagHold = true, flagTransf = false,flagInit = true, num = null, headerIdCamp, headerNomCamp, calltypeId, flagPausa = 0, fromUser, wId, lastPause, uid = "";
var sipStatus = document.getElementById('SipStatus');var callStatus = document.getElementById('CallStatus');var local = document.getElementById('localAudio');var remoto = document.getElementById('remoteAudio');var displayNumber = document.getElementById("numberToCall"); var pauseButton = document.getElementById("Pause");

function suma(a, b) {
	return a+b;
}

function updateButton(btn,clsnm,inht) {
	 	 btn.className = clsnm;
	 	 var lastval = btn.innerHTML;
	 	 btn.innerHTML = inht;
	 	 return lastval;
}

$(function() {

	$("#modalWebCall").modal('show');
	/*
	ESTADO_OFFLINE = 1    """Agente en estado offline"""
	ESTADO_ONLINE = 2    """Agente en estado online"""
	ESTADO_PAUSA = 3    """Agente en estado pausa"""
	*/
	function changeStatus(status, idagente) {
		$.ajax({
			type: "get",
			url: "/agente/cambiar_estado?estado="+status+"&pk_agente="+idagente,
			contentType: "text/html",
			success: function (msg) {

			},
			error: function (jqXHR, textStatus, errorThrown) {
									debugger;
									console.log("Error al ejecutar => " + textStatus + " - " + errorThrown);
			}
		});
	}

	var modifyUserStat = document.getElementById("UserStatus");
	$("#redial").prop('disabled', true);
	$('#modalSelectCmp').modal('hide');
  var estado = JSON.stringify({'status' : 'online'});

	 $("#SignCall").click(function () {
	   $("#modalSignCall").modal('show');
	 });

	 $("#SaveSignedCall").click(function () {
	 	 var desc = $("#SignDescription").val();// sign subject
		 var URl = "grabacion/marcar/";
		 var data2 =  {"uid": uid, "descripcion": desc};
	 	 $.ajax({
	 	   url: URl,
	 	   type: 'POST',
       dataType: 'application/json',
       data: data2,
       succes: function (msg) {

	     },
    	 error: function (jqXHR, textStatus, errorThrown) {
         console.log("Error al ejecutar => " + textStatus + " - " + errorThrown);
    	 }
	 	 });
	   $("#modalSignCall").modal('hide');
	   campid = idagt = desc = null;
	 });

  $("#Resume").click(function() {
  	num = "0077UNPAUSE";
    makeCall();
  });

  $("#setPause").click(function() {
  	var pausa = $("#pauseType").val().toUpperCase();
  	if(pausa.indexOf(' ')) {
  		pausa = pausa.replace(' ','');
  	}
    num = "0077" + pausa;
    makeCall();
  });

  if($("#sipExt").val() && $("#sipSec").val()) {
    config = {
      uri : "sip:"+$("#sipExt").val()+"@"+KamailioIp,
      ws_servers : "wss://"+KamailioIp+":443",
      password : $("#sipSec").val(),
      hack_ip_in_contact: true,
      session_timers: false,
			pcConfig: {
				rtcpMuxPolicy: 'negotiate'}
    };
    userAgent = new JsSIP.UA(config);
    sesion = userAgent.start();
  }

  $("#CallList").click(function() {
    $("#modalCallList").modal('show');
  });

  $(".key").click(function(e) {
    var numPress = "";
    if(displayNumber.value === "") {
      numPress = e.currentTarget.childNodes[0].data;
    } else {
      numPress = displayNumber.value;
      numPress += e.currentTarget.childNodes[0].data;
    }
    displayNumber.value = numPress;
  });

  //Connects to the WebSocket server
  userAgent.on('registered', function(e) { // cuando se registra la entidad SIP
    setSipStatus("greydot.png", "  No account", sipStatus);
  	updateButton(modifyUserStat, "label label-success", "Online");
    num = "0077LOGIN";
    makeCall();
    $("#sendMessage").prop('disabled', false);
    $("#chatMessage").prop('disabled', false);
    iconStatus.parentNode.removeChild(iconStatus);
    textSipStatus.parentNode.removeChild(textSipStatus);
    setSipStatus("greendot.png", "  Registered", sipStatus);
    defaultCallState();
  });

  userAgent.on('registrationFailed', function(e) {  // cuando falla la registracion
    setSipStatus("redcross.png", "  Registration failed", sipStatus);
  });

  userAgent.on('newRTCSession', function(e) {       // cuando se crea una sesion RTC

		var objLastPause = {};
		objLastPause.LastStatusAgent = $("#UserStatus").html();
		objLastPause.LastStatusAgentClass = $("#UserStatus").attr('class');
		objLastPause.LastBtnStatusPause = $("#Pause").prop('disabled');
		objLastPause.LastBtnStatusResume = $("#Resume").prop('disabled');
		objLastPause.LastBtnStatusSipLogout = $("#sipLogout").prop('disabled');
	  var originHeader = "";

    function saveCall(callerOrCalled) {
    	$.ajax({
          type: "get",
	   	    url: "/duracion/llamada/",
	   	    contentType: "text/html",
	   	    data : "duracion=" + $("#horaC").html() + $("#minsC").html() + $("#segsC").html() + "&agente="+$("#idagt").val()+"&numero_telefono="+callerOrCalled+"&tipo_llamada="+calltypeId,
	   	    success: function (msg) {
	   //	 	    reinicio3($("#horaC"), $("#minsC"), $("#segsC"));
	   	 	    $("#call_list").html(msg);
	   	    },
	   	    error: function (jqXHR, textStatus, errorThrown) {
	          debugger;
	          console.log("Error al ejecutar => " + textStatus + " - " + errorThrown);
	        }
        });
    }
    function originToId(origin) {
      var id = '';
			var origin = origin;
			if(origin) {
				if(origin.search("DIALER") === 0) {
					origin = "DIALER";
				}
			}
      switch(origin) {
				case "CLICK2CALL":
  			  id = 5;
  		  	break;
  		  case "DIALER":
  			  id = 2;
  		  	break;
  			case "IN":
  		    id = 3;
  		  	break;
			  case "ICS":
  				id = 1;
  				break;
 				default:
  			  id = 4;
  			  break;
  		}
  	  return id;
    }
    function reinicio(horaDOM, minDOM, segDOM) {
	    clearInterval(control);
	    centesimasP = 0;
	    segundosP = 0;
	    minutosP = 0;
	    segDOM.html(":00");
	    minDOM.html(":00");
	    horaDOM.html("00");
  	}
    //dar solucion a la repeticion de codigo, esto ya existe en main.js
  	function parar2() {
	 		clearInterval(control2);
	 	}
	 	function parar3() {
	    clearInterval(control3);
	 	}
	 	function inicio2() {
	    control2 = setInterval(cronometro2, 1000);
	 	}
	 	function inicio3() {
	 		control3 = setInterval(cronometro3, 1000);
	 	}
	 	//****************************CRONOMETRO DE Pausas***********************************
    function cronometro2() {
	    if (centesimasP < 59) {
	      centesimasP++;
	        if (centesimasP < 10) {
	          centesimasP = "0" + centesimasP;
	        }
	        $("#segsP").html(":" + centesimasP);
	    }
	    if (centesimasP == 59) {
	      centesimasP = -1;
	    }
	    if (centesimasP == 0) {
	      segundosP++;
	        if (segundosP < 10) {
	          segundosP = "0" + segundosP;
	        }
	        $("#minsP").html(":" + segundosP);
	    }
	    if (segundosP == 59) {
	      segundosP = -1;
	    }
	    if ((centesimasP == 0) && (segundosP == 0)) {
	      minutosP++;
	        if (minutosP < 10) {
	          minutosP = "0" + minutosP;
	        }
	        $("#horaP").html("" + minutosP);
	    }
	  }
	 //****************************CRONOMETRO DE LLAMADA***********************************
	 function cronometro3() { // Cronometro embebido en el webphone
	     if (centesimasC < 59) {
	         centesimasC++;
	         if (centesimasC < 10) {
	             centesimasC = "0" + centesimasC;
	         }
	         $("#segsC").html(":" + centesimasC);
	     }
	     if (centesimasC == 59) {
	         centesimasC = -1;
	     }
	     if (centesimasC == 0) {
	         segundosC++;
	         if (segundosC < 10) {
	             segundosC = "0" + segundosC;
	         }
	         $("#minsC").html(":" + segundosC);
	     }
	     if (segundosC == 59) {
	         segundosC = -1;
	     }
	     if ((centesimasC == 0) && (segundosC == 0)) {
	         minutosC++;
	         if (minutosC < 10) {
	             minutosC = "0" + minutosC;
	         }
	         $("#horaC").html("" + minutosC);
	     }
	 }

	 function reinicio3(horaDOM, minDOM, segDOM) { // Cronometro embebido en el webphone
	   clearInterval(control);
	   centesimasC = 0;
	   segundosC = 0;
	   minutosC = 0;
	   segDOM.html(":00");
	   minDOM.html(":00");
	   horaDOM.html("00");
   }
	 	//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    e.session.on("failed",function(e) {  // cuando falla el establecimiento de la llamada
      $("#aTransfer").prop('disabled', true);
      $("#bTransfer").prop('disabled', true);
      $("#onHold").prop('disabled', true);
      $("#modalReceiveCalls").modal('hide');
      Sounds("","stop");
    });
      if(e.originator=="remote") {         // Origen de llamada Remoto
      	entrante = true;
      	if(e.request.headers.Wombatid) {
      		wId = e.request.headers.Wombatid[0].raw;
      	}
      	if(e.request.headers.Origin) {
      	  originHeader = e.request.headers.Origin[0].raw;
      	}
      	if (e.request.headers.Idcliente) {
      		var leadIdHeader = e.request.headers.Idcliente[0].raw;
      	}
      	if (e.request.headers.Idcamp) {
      		var CampIdHeader = e.request.headers.Idcamp[0].raw;
      		$("#idCamp").val(CampIdHeader);
      	}

        if(e.request.headers.Uidgrabacion) {
	        uid = e.request.headers.Uidgrabacion[0].raw;
        }
        fromUser = e.request.headers.From[0].raw;
        var endPos = fromUser.indexOf("@");
        var startPos = fromUser.indexOf(":");
        fromUser = fromUser.substring(startPos+1,endPos);

        if(CampIdHeader) {
        	if(leadIdHeader) {
						if(originHeader === "DIALER-FORM") {
							getData(CampIdHeader, leadIdHeader, $("#idagt").val(), wId);
						} else if (originHeader === "DIALER-SITIOEXTERNO") {
							var linkaddress = e.request.headers.Sitioexterno[0].raw;
							getIframe(linkaddress);
						} else if (originHeader === "DIALER-JSON") {

						} else if (originHeader === "CLICK2CALL") {
						  getData(CampIdHeader, leadIdHeader, $("#idagt").val(), 0);
						}
        	} else {
        		if(fromUser !== "Unknown") {
        	    processCallid(fromUser);
        		} else {
        			getBlankFormCamp(CampIdHeader);
        		}
        	}
        }

        $("#callerid").text(fromUser);
        if($("#modalWebCall").is(':visible')) {
          $("#modalReceiveCalls").modal('show');
        } else {
          $("#modalWebCall").modal('show');
          $("#modalReceiveCalls").modal('show');
        }
        Sounds("In", "play");
        var atiendoSi = document.getElementById('answer');
        var atiendoNo = document.getElementById('doNotAnswer');
        var session_incoming = e.session;

        session_incoming.on('addstream',function(e) {       // al cerrar el canal de audio entre los peers
        	$("#Pause").prop('disabled',true);
        	$("#Resume").prop('disabled',true);
        	$("#sipLogout").prop('disabled',true);
        	lastPause = $("#UserStatus").html();
        	updateButton(modifyUserStat, "label label-primary", "OnCall");
          remote_stream = e.stream;
          remoto = JsSIP.rtcninja.attachMediaStream(remoto, remote_stream);
        });

        var options = {'mediaConstraints': {'audio': true, 'video': false}};
        calltypeId = originToId(originHeader);
        processOrigin(originHeader, options, fromUser);

        atiendoSi.onclick = function() {
          $("#modalReceiveCalls").modal('hide');
          session_incoming.answer(options);
          setCallState("Connected to " +fromUser , "orange");
          Sounds("","stop");
        };

        atiendoNo.onclick = function() {
          $("#modalReceiveCalls").modal('hide');
          if($("#autopause").val() === "True") {

          }
          userAgent.terminateSessions();
          defaultCallState();
        };

        function processOrigin(origin, opt, from) {
			  	var options = opt;
					var origin = origin;
					if(origin) {
						if(origin.search("DIALER") === 0) {
							origin = "DIALER";
						}
					}
  				switch(origin) {
  					case "DIALER":
  						var dialerTag = document.getElementById("auto_attend_DIALER");
  						if(dialerTag.value === "True") {
  							$("#modalReceiveCalls").modal('hide');
  			  			session_incoming.answer(options);
          			setCallState("Connected to " + from, "orange");
          			Sounds("","stop");
  						}
  		  			break;
  					case "IN":
  		  			var inboundTag = document.getElementById("auto_attend_IN");
  		  			if(inboundTag.value === "True") {
  		  				$("#modalReceiveCalls").modal('hide');
  			  			session_incoming.answer(options);
          			setCallState("Connected to " + from, "orange");
          			Sounds("","stop");
  						}
  		  			break;
			  		case "ICS":
  						var icsTag = document.getElementById("auto_attend_ICS");
  						if(icsTag.value === "True") {
			  				$("#modalReceiveCalls").modal('hide');
  			  			session_incoming.answer(options);
          			setCallState("Connected to " + from, "orange");
          			Sounds("","stop");
  						}
  		  			break;
						case "CLICK2CALL":
						  $("#modalReceiveCalls").modal('hide');
							session_incoming.answer(options);
							setCallState("Connected to " + from, "orange");
							Sounds("","stop");
						  break;
  				}
  			}

      } else {
      	calltypeId = originToId(null);
        Sounds("Out", "play");
        var session_outgoing = e.session;
      }

      e.session.on("accepted", function() { 			// cuando se establece una llamada
        Sounds("", "stop");
        $("#aTransfer").prop('disabled', false);
        $("#bTransfer").prop('disabled', false);
        $("#onHold").prop('disabled', false);

        if(num.substring(4,0) != "0077") {
			//		inicio3();
	       	$("#Pause").prop('disabled',true);
	       	$("#Resume").prop('disabled',true);
	       	$("#sipLogout").prop('disabled',true);
	       	lastPause = $("#UserStatus").html();
	       	updateButton(modifyUserStat, "label label-primary", "OnCall");
		    }
      });

			var clickHold = document.getElementById("onHold");
	  	clickHold.onclick = function () {
				if(flagHold) {
	  	 		flagHold = false;
					e.session.sendDTMF("*");
		      e.session.sendDTMF("2");
		      setTimeout(transferirHold(e), 1000);
	  	 	} else {
	  	 	  flagHold = true;
					e.session.sendDTMF("*");
		      e.session.sendDTMF("1");
	  	 	}
			};

		var one = document.getElementById("1");
		one.onclick = function() {
			e.session.sendDTMF('1');
		};

		var two = document.getElementById("2");
		two.onclick = function() {
			e.session.sendDTMF('2');
		};

		var three = document.getElementById("3");
		three.onclick = function() {
			e.session.sendDTMF('3');
		};

		var four = document.getElementById("4");
		four.onclick = function() {
			e.session.sendDTMF('4');
		};

		var five = document.getElementById("5");
		five.onclick = function() {
			e.session.sendDTMF('5');
		};

		var six = document.getElementById("6");
		six.onclick = function() {
			e.session.sendDTMF('6');
		};

		var seven = document.getElementById("7");
		seven.onclick = function() {
			e.session.sendDTMF('7');
		};

		var eight = document.getElementById("8");
		eight.onclick = function() {
			e.session.sendDTMF('8');
		};

		var nine = document.getElementById("9");
		nine.onclick = function() {
			e.session.sendDTMF("9");
		};

    var aTransf = document.getElementById("aTransfer");
    aTransf.onclick = function() {
      flagTransf = true;
      e.session.sendDTMF("*");
      e.session.sendDTMF("2");
      setTimeout(transferir(e), 3000);
    };

    var bTransf = document.getElementById("bTransfer");
    bTransf.onclick = function() {
      flagTransf = true;
      e.session.sendDTMF("#");
      e.session.sendDTMF("#");
      setTimeout(transferir(e), 3000);
    };

    function transferir(objRTCsession) {
      objRTCsession.session.sendDTMF(displayNumber.value);
    }

		function transferirHold(objRTCsession) {
      objRTCsession.session.sendDTMF('*098');
    }

		e.session.on("ended",function() {               // Cuando Finaliza la llamada
			if(entrante) {
				if(fromUser) { // fromUser es para entrantes
					if(lastPause === "Online" && fromUser.substring(4,0) != "0077") {
						saveCall(fromUser);
						num = '';
						fromUser = "";
						$("#Pause").prop('disabled',false);
						$("#Resume").prop('disabled',true);
						$("#sipLogout").prop('disabled',false);
						updateButton(modifyUserStat, "label label-success", "Online");
					} else if(lastPause === "OnCall") {
						saveCall(fromUser);
						num = '';
						fromUser = "";
						$("#Pause").prop('disabled',false);
						$("#Resume").prop('disabled',true);
						$("#sipLogout").prop('disabled',false);
						updateButton(modifyUserStat, "label label-success", "Online");
					} else {
						//reinicio3();
						fromUser = "";
						$("#Pause").prop('disabled',true);
						$("#Resume").prop('disabled',false);
						$("#sipLogout").prop('disabled',false);
						updateButton(modifyUserStat, "label label-danger", lastPause);
					}
					if(fromUser.substring(4,0) != "0077") {
							if ($("#auto_pause").val() == "True") {//Si es un agente predictivo
								changeStatus(3, $("#idagt").val());
						    num = "0077ACW";
						    makeCall();
						    entrante = false;
								$("#Pause").prop('disabled',true);
								$("#Resume").prop('disabled',false);
								$("#sipLogout").prop('disabled',false);
								updateButton(modifyUserStat, "label label-danger", "ACW");
								inicio2();
					//			parar3();
								if($("#auto_unpause").val() != 0) {
							    var timeoutACW = $("#auto_unpause").val();
							    timeoutACW = timeoutACW * 1000;
							    var toOnline = function() {
							      num = "0077UNPAUSE";
							      if($("#UserStatus").html() === "ACW") {
							        makeCall();
							        $("#Resume").trigger('click');
							      }
							    };
							    setTimeout(toOnline, timeoutACW);
							  }
							} // si no es agente predictivo....
					} else {
//					    reinicio3($("#horaC"), $("#minsC"), $("#segsC"));
					}
				}
			} else { // si NO es una llamada entrante
				if (num) { // num para salientes
					if (num.substring(4,0) != "0077") {
						saveCall(num);
						if (lastPause != "Online") {
							num = '';
							$("#Pause").prop('disabled',true);
							$("#Resume").prop('disabled',false);
							$("#sipLogout").prop('disabled',false);
							updateButton(modifyUserStat, "label label-danger", lastPause);
						} else {
							$("#Pause").prop('disabled',false);
							$("#Resume").prop('disabled',true);
							$("#sipLogout").prop('disabled',false);
							updateButton(modifyUserStat, "label label-success", lastPause);
						}
						if ($("#auto_pause").val() == "True") {//Si es un agente predictivo
							changeStatus(3, $("#idagt").val());
					        num = "0077ACW";
					        makeCall();
					        entrante = false;
							$("#Pause").prop('disabled',true);
							$("#Resume").prop('disabled',false);
							$("#sipLogout").prop('disabled',false);
							updateButton(modifyUserStat, "label label-danger", "ACW");
		//			        inicio2();
							if($("#auto_unpause").val() != 0) {
								var timeoutACW = $("#auto_unpause").val();
								timeoutACW = timeoutACW * 1000;
								var toOnline = function() {
									num = "0077UNPAUSE";
									if($("#UserStatus").html() === "ACW") {
										makeCall();
										$("#Resume").trigger('click');
									}
								};
								setTimeout(toOnline, timeoutACW);
							}
					    }
					} else {
			//		   reinicio3($("#horaC"), $("#minsC"), $("#segsC"));
					}
			    }
		    }
		defaultCallState();
    });

  });

	$("#numberToCall").bind("keypress", function(event) {
		if(event.which == 13) {
			event.preventDefault();
			entrante = false;
			if(displayNumber.value != "") {
				displayNumber.style.borderColor = "black";
	      num = displayNumber.value;
	      lastDialedNumber = num;
				if($("#campAssocManualCall").html() == "") {
					$("#modalSelectCmp").modal("show");
				} else {
					headerIdCamp = $("#cmpList").val();
			  	$("#idCamp").val(headerIdCamp);
					var nombrecamp = $("#cmpList option:selected").html();
					nombrecamp = nombrecamp.substring(1);
			  	headerNomCamp = $("#idCamp").val() + '_' + nombrecamp;
			    $("#redial").prop('disabled',false);
			  	makeCall();
				}
			} else {
	      displayNumber.style.borderColor = "red";
			}
		}
	});

  $("#redial").click(function () {// esto es para enviar un Invite/llamada
  	entrante = false;
  	num = lastDialedNumber;
		if($("#campAssocManualCall").html() == "") {
  	  $("#modalSelectCmp").modal("show");
    }
		makeCall();
  });

  $("#endCall").click(function() {
    Sounds("", "stop");
    userAgent.terminateSessions();
    defaultCallState();
  });

  $("#call").click(function(e) {
  	entrante = false;
		if(displayNumber.value != "") {
			displayNumber.style.borderColor = "black";
      num = displayNumber.value;
      lastDialedNumber = num;
			if($("#campAssocManualCall").html() == "") {
				$("#modalSelectCmp").modal("show");
			} else {
				headerIdCamp = $("#cmpList").val();
		  	$("#idCamp").val(headerIdCamp);
				var nombrecamp = $("#cmpList option:selected").html();
				nombrecamp = nombrecamp.substring(1);
				headerNomCamp = $("#idCamp").val() + '_' + nombrecamp;
		    $("#redial").prop('disabled',false);
		  	makeCall();
				getFormManualCalls($("#idCamp").val(), $("#idagt").val(), num);
			}
		} else {
      displayNumber.style.borderColor = "red";
		}
  });

	$("#changeCampAssocManualCall").click(function () {
		$("#modalSelectCmp").modal("show");
	});

  $("#SelectCamp").click(function () {
		if(displayNumber.value != "") {
			$("#modalSelectCmp").modal("hide");
	  	headerIdCamp = $("#cmpList").val();
	  	$("#idCamp").val(headerIdCamp);
			var nombrecamp = $("#cmpList option:selected").html();
			nombrecamp = nombrecamp.substring(1);
			headerNomCamp = $("#idCamp").val() + '_' + nombrecamp;
	    $("#redial").prop('disabled',false);
			$("#campAssocManualCall").html(headerNomCamp);
			getFormManualCalls($("#idCamp").val(), $("#idagt").val(), displayNumber.value);
	  	makeCall();
		} else {
			$("#modalSelectCmp").modal("hide");
			headerIdCamp = $("#cmpList").val();
	  	$("#idCamp").val(headerIdCamp);
			var nombrecamp = $("#cmpList option:selected").html();
			nombrecamp = nombrecamp.substring(1);
			headerNomCamp = $("#idCamp").val() + '_' + nombrecamp;
	    $("#redial").prop('disabled',false);
			$("#campAssocManualCall").html(headerNomCamp);
		}
  });

  function makeCall() {
    eventHandlers = {
      'confirmed':  function(e) {
        // Attach local stream to selfView
                    local.src = window.URL.createObjectURL(sesion.connection.getLocalStreams()[0]);
                    },
      'addstream':  function(e) {
										if(num.substring(4,0) != "0077"){
											setCallState("Connected to " + num, "orange");
										} else {
											setCallState("Connected", "orange");
										}
                    var stream = e.stream;
                    // Attach remote stream to remoteView
                    remoto.src = window.URL.createObjectURL(stream);
                    },
      'failed': function(data) {
                  if (data.cause === JsSIP.C.causes.BUSY) {
                    Sounds("", "stop");
      					  	Sounds("", "play");
                  	setCallState("Ocupado, intenta mas tarde", "orange");
                   	setTimeout(defaultCallState, 5000);
                  } else if (data.cause === JsSIP.C.causes.REJECTED) {
                    setCallState("Rechazo, intenta mas tarde", "orange");
                    setTimeout(defaultCallState, 5000);
                  } else if (data.cause === JsSIP.C.causes.UNAVAILABLE) {
                      setCallState("Unavailable", "red");
                      setTimeout(defaultCallState, 5000);
                  } else if (data.cause === JsSIP.C.causes.NOT_FOUND) {
                    setCallState("Error, revisa el numero discado", "red");
                    setTimeout(defaultCallState, 5000);
                  } else if (data.cause === JsSIP.C.causes.AUTHENTICATION_ERROR) {
                    setCallState("Auth error", "red");
                    setTimeout(defaultCallState, 5000);
                  } else if (data.cause === JsSIP.C.causes.MISSING_SDP) {
                    setCallState("Missing sdp", "red");
                    setTimeout(defaultCallState, 5000);
                  } else if (data.cause === JsSIP.C.causes.ADDRESS_INCOMPLETE) {
                    setCallState("Address incomplete", "red");
                    setTimeout(defaultCallState, 5000);
                  } else if (data.cause === "SIP Failure Code") {
      							  setCallState("JsSIP SIP Failure code (500)", "red");
                    	setTimeout(defaultCallState, 5000);
                  }
                }
    };
    opciones = {
      'eventHandlers': eventHandlers,
      'mediaConstraints': {
                'audio': true,
                'video': false
              },
      'extraHeaders':['Idcamp:'+headerIdCamp, 'Nomcamp:'+headerNomCamp],
			pcConfig: {rtcpMuxPolicy: 'negotiate'}
    };
    //Mando el invite/llamada
     if(flagInit === true) {
       flagInit = false;
       sesion = userAgent.call("sip:"+num+"@"+KamailioIp, opciones);
     } else {
       sesion = userAgent.call("sip:"+num+"@"+KamailioIp, opciones);
       setCallState("Calling.... "+num, "yellowgreen");
       displayNumber.value = "";
     }
  }

  function setCallState(estado, color) {
    callSipStatus.parentNode.removeChild(callSipStatus);
    callSipStatus = document.createElement("em");
    var textCallSipStatus = document.createTextNode(estado);
    callSipStatus.style.color = color;
		callSipStatus.id = "dial_status";
    callSipStatus.appendChild(textCallSipStatus);
    callStatus.appendChild(callSipStatus);
  }

  function defaultCallState() {
    if(callStatus.childElementCount > 0) {
      callSipStatus.parentNode.removeChild(callSipStatus);
    }
    callSipStatus = document.createElement("em");
    textCallSipStatus = document.createTextNode("Idle");
    callSipStatus.style.color = "#80FF00";
		callSipStatus.id = "dial_status";
    callSipStatus.appendChild(textCallSipStatus);
    callStatus.appendChild(callSipStatus);
    $("#aTransfer").prop('disabled', true);
    $("#bTransfer").prop('disabled', true);
    $("#onHold").prop('disabled', false);
  }

  function setSipStatus(img, state, elem) {
    if(elem.childElementCount > 0) {
      var hijo1 = document.getElementById("textSipStatus");
      var hijo2 = document.getElementById("imgStatus");
      elem.removeChild(hijo1);
      elem.removeChild(hijo2);
    }
    iconStatus = document.createElement('img');
    textSipStatus = document.createTextNode(state);
    iconStatus.id = "imgStatus";
    textSipStatus.id = "textSipStatus";
    elem.style.color="white";
    iconStatus.src = "../static/ominicontacto/Img/"+img;
    elem.appendChild(iconStatus);
    elem.appendChild(textSipStatus);
  }

  function Sounds(callType, action) {
    var ring = null;
    if(action === "play") {
      if(callType === "In") {
        ring = document.getElementById('RingIn');
        ring.play();
      } else if(callType === "Out") {
        ring = document.getElementById('RingOut');
        ring.play();
      } else {
      	ring = document.getElementById('RingBusy');
        ring.play();
      }
    } else {
        ring = document.getElementById('RingIn');
        ring.pause();
        ring = document.getElementById('RingOut');
        ring.pause();
        ring = document.getElementById('RingBusy');
        ring.pause();
    }
  }

  function getBlankFormCamp(campid) {
    var url = '/campana/'+campid+'/formulario_nuevo/';
    $("#dataView").attr('src', url);
  }

	function processCallid(callerid) {
  	var url = "/campana/selecciona/";
  	$("#dataView").attr('src', url);
  }

  function getData(campid, leadid,agentid, wombatId) {
    var tipoGestion = "/update/";
    if ($("#campanaType").length > 0) {
      // comprobamos si la campaña es preview, y en ese caso renderizamos directamente
      // el formulario de creación de calificación en vez del de creación
      tipoGestion = "/create/";
    }
    var url = "/formulario/"+campid+"/calificacion/"+leadid+tipoGestion+agentid+"/"+wombatId+"/";
    $("#dataView").attr('src', url);
  }

	function getFormManualCalls(idcamp, idagt, tel) {
		var url = "/campana_manual/" + idcamp + "/calificacion/" + idagt + "/create/" + tel + "/";
		$("#dataView").attr('src', url);
	}

	function getIframe(url) {
		$("#dataView").attr('src', url);
		/*tipo_interac; //= 2 "sitioexterno"
		// 1 "url comun"
		campana.sitio_externo.url
		sitio_externo;
		nombre;
		fecha_inicio;
		fecha_fin;
		calificacion*/
	}

  function sendStatus(pauseType,agent,statusAg) {
  	$.ajax({
      type: "get",
	   	url: "///",
	   	contentType: "text/html",
	   	data : "agente=" + agent + "&estado="+statusAg+"&tipo_pausa="+pauseType,
	   	success: function (msg) {

	   	},
	   	error: function (jqXHR, textStatus, errorThrown) {
	      debugger;
	      console.log("Error al ejecutar => " + textStatus + " - " + errorThrown);
	    }
    });
  }

});
