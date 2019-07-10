let genresList = [];

function hide(element) {
    let op = 1,
    	timer = setInterval(function () {
	        if (op <= 0.01){
	            clearInterval(timer);
	            element.style.display = 'none';
	        }
	        element.style.opacity = op;
	        op = op - 0.035;
    }, 1);
}

function show(element) {
    let op = 0,
    	timer = setInterval(function () {
	        if (op >= 1){
	            clearInterval(timer);
	        }
	        element.style.opacity = op;
	        element.style.display = 'block';
	        op = op + 0.035;
    }, 1);
}

function refreshArtistList(genresList) {
	const artistsList = document.querySelectorAll('.artists ul li');

	if(genresList.length == 0) {
		for (artist of artistsList) {
			show(artist);
		}
		return;
	}

	for (artist of artistsList) {
		hide(artist);

		let artistGenres = artist.querySelector('.artist_name').dataset.genres;

		const genresArr = artistGenres.split(',');
		genresArr.pop();


		for (genre of genresList) {
			if(genresArr.indexOf(genre) !== -1) {
				show(artist);
			}
		}
	}
}

function genreClick(e) {
	e.preventDefault();
	const genre = e.target;
	if(genre.tagName === 'A') {
		genre.classList.toggle('active');

		let genreText = genre.textContent;

		if(genre.classList.contains('active')) {
			genresList.push(genreText);
		} else {
			let index = genresList.indexOf(genreText);
			if (index !== -1) genresList.splice(index, 1);
		}

		refreshArtistList(genresList);
	}
}

function artistClick(e) {
	e.preventDefault();
	const artist = e.target,
		modalBodyInfo = document.querySelector('.modal-body .info_block'),
		modalBodySimilar = document.querySelector('.modal-body .similar_block'),
		tilleBlock = document.querySelector('h5.modal-title');

	if(artist.tagName === 'A') {
		modalBodyInfo.innerText = 'Данные загружаются...';
		modalBodySimilar.innerText = '';
		tilleBlock.innerText = '';

		let artist_id = artist.href.split('/').pop();

		fetch(`/getInfo/${artist_id}`)
		  .then(function(response) {
		    console.log(response.headers.get('Content-Type')); // application/json
		    console.log(response.status); // 200

		    return response.json();
		   })
		  .then(function(artistInfo) {
		    let info = artistInfo.info,
		    	title = artistInfo.title,
		    	similarStringify = JSON.stringify(artistInfo.similar),
		    	similarParsed = JSON.parse(similarStringify);

		    tilleBlock.innerHTML = title.name;
		    tilleBlock.append(title.like)

		    modalBodyInfo.innerText = info;
		    modalBodySimilar.innerHTML = '<h2>Похожие исполнители</h2>';


		    for (similarArtist of similarParsed) {
		    	let key = Object.keys(similarArtist)[0],
		    		thisArtist = similarArtist[key],
		    		wrap = document.createElement('div'),
		    		image = document.createElement('img'),
		    		genres = document.createElement('div'),
		    		name = document.createElement('h3');
		    		

		    	wrap.classList.add('similar_wrapper');
		    	image.src = thisArtist.avatar;
		    	genres.innerText = thisArtist.genres;
		    	name.innerHTML = `<a href='${thisArtist.href}' target='_blank'>${key}</a>`;

		    	wrap.append(name);
		    	wrap.append(genres);
		    	wrap.append(image);
		    	
		    	
		    	modalBodySimilar.append(wrap);
		    }
		    

		  })
		  .catch( alert );
		  $('#exampleModalLong').modal('toggle');
	}
}

document.addEventListener('DOMContentLoaded', ()=>{

	const genresBlock = document.querySelector('.genres'),
		artistsBlock = document.querySelector('.artists');

	genresBlock.addEventListener('click', genreClick);
	artistsBlock.addEventListener('click', artistClick);





















});