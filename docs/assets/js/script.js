Element.prototype.getElementById = function(id) {
	return this.querySelector("#"+id);
}

mascotART = function(mascot) {
	document.getElementById("m_" + mascot).getElementById("ART").style.display="block";
	document.getElementById("m_" + mascot).getElementById("VA").style.display="none";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[0].style.pointerEvents = "none";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[0].style.backgroundPositionY = "0";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[1].style.pointerEvents = "auto";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[1].style.backgroundPositionY = "-14px";
}

mascotVA = function(mascot) {
	document.getElementById("m_" + mascot).getElementById("ART").style.display="none";
	document.getElementById("m_" + mascot).getElementById("VA").style.display="block";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[0].style.pointerEvents = "auto";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[0].style.backgroundPositionY = "-14px";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[1].style.pointerEvents = "none";
	document.getElementById("m_" + mascot).getElementById("BTN").getElementsByTagName('div')[1].style.backgroundPositionY = "0";
}

mascotFilter = function(filter) {
	switch(filter){
		case 'all':
			document.getElementById("f_humanoid").style.display="block";
			document.getElementById("f_animal").style.display="block";
			break;
		case 'humanoid':
			document.getElementById("f_humanoid").style.display="block";
			document.getElementById("f_animal").style.display="none";
			break;
		case 'animal':
			document.getElementById("f_humanoid").style.display="none";
			document.getElementById("f_animal").style.display="block";
			break;
	}
}

function mascotHover(mascot) {
	document.getElementById("m_" + mascot).getElementsByTagName('img')[0].setAttribute('src', 'assets/images/mascots/' + mascot + '-wave.png');
}

function mascotUnhover(mascot) {
	document.getElementById("m_" + mascot).getElementsByTagName('img')[0].setAttribute('src', 'assets/images/mascots/' + mascot + '.png');
}