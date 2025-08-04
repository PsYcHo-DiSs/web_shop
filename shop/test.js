function createArtwork(title, artist, year, type, size, museum) {
    let art = {
        title: title,
        artist: artist,
        year: year,
        type: type,
        size: size,
        museum: museum,
        details: {
            size: size,
            museum: museum,
            exhibitions: [],
        },
        addExhibition(mus_name) {
            this.details.exhibitions.push(mus_name)
        },
        getInfo() {
            if (this.details.exhibitions) {
                return `Название: ${this.title}, Автор: ${this.artist}, Год: ${this.year}, Тип: ${this.type}, Размер: ${this.details.size} м, Музей: ${this.details.museum}, Выставки: Нет`
            }
            else {
                return `Название: ${this.title}, Автор: ${this.artist}, Год: ${this.year}, Тип: ${this.type}, Размер: ${this.details.size} м, Музей: ${this.details.museum}, Выставки: ${this.details.exhibitions}`
            }

        }
    }
return art
}

// Не забывайте!
// Функция trim() удаляет лишние пробелы в начале и конце строки.
// Это помогает избежать некорректного ввода данных с пробелами или другими символами, например: " Мона Лиза " -> "Мона Лиза".


let title = prompt();
let artist = prompt();
let year = parseInt(prompt());
let type = prompt();
let size = prompt(); // Например, "0.77x0.53"
let museum = prompt();
let artwork = createArtwork(title, artist, year, type, size, museum);
console.log(artwork.getInfo());

// Добавление новой выставки
let newMuseum = prompt();
artwork.addExhibition(newMuseum);
console.log("После добавления новой выставки:", artwork.getInfo());