let genresList = [];

function refreshArtistList(genresList) {
	const artistsList = document.querySelectorAll('.artists ul li');

	if(genresList.length == 0) {
		for (artist of artistsList) {
			artist.classList.remove('hidden');
		}
		return;
	}

	for (artist of artistsList) {
		artist.classList.add('hidden');
		let artistGenres = artist.querySelector('.artist_name').dataset.genres;

		const genresArr = artistGenres.split(',');
		genresArr.pop();



		for (genre of genresList) {
			if(genresArr.indexOf(genre) !== -1) {
				artist.classList.remove('hidden');
			}
		}
	}

}

function genreClick(e) {
	e.preventDefault();
	const genre = e.target;
	if(genre.tagName === 'A') {
		genre.classList.toggle('active');
	}

	let genreText = genre.textContent;

	if(genre.classList.contains('active')) {
		genresList.push(genreText);
	} else {
		let index = genresList.indexOf(genreText);
		if (index !== -1) genresList.splice(index, 1);
	}

	refreshArtistList(genresList);
}

document.addEventListener('DOMContentLoaded', ()=>{
	const genres = document.querySelector('.genres');
	genres.addEventListener('click', genreClick);






















});