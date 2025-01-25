document.addEventListener('DOMContentLoaded', () => {
    // Funzione per creare una card anime
    function createAnimeCard(anime, isCalendar = false) {
        console.log('Creating card for:', anime); // Debug log
        
        const card = document.createElement('div');
        card.className = 'anime-card';
        
        if (isCalendar) {
            card.innerHTML = `
                <img src="${anime.poster}" alt="${anime.titolo}" onerror="this.src='https://via.placeholder.com/200x300'">
                <div class="anime-info">
                    <h3>${anime.titolo}</h3>
                    <p>${anime.episodio}</p>
                    <p>Ora: ${anime.ora}</p>
                </div>
            `;
        } else {
            card.innerHTML = `
                <img src="${anime.poster}" alt="${anime.titolo}" onerror="this.src='https://via.placeholder.com/200x300'">
                <div class="anime-info">
                    <h3>${anime.titolo}</h3>
                    ${anime.info ? `
                        <p>Data: ${anime.info.data_uscita}</p>
                        <p>Stato: ${anime.info.stato}</p>
                        <p>Voto: ${anime.info.voto}</p>
                        <p class="descrizione">${anime.info.descrizione}</p>
                    ` : ''}
                    ${anime.episodio ? `<p>Episodio: ${anime.episodio}</p>` : ''}
                </div>
            `;
        }
        
        return card;
    }

    // Funzione per mostrare/nascondere il loader
    function toggleLoader(sectionId, show) {
        const section = document.querySelector(sectionId);
        let loader = section.querySelector('.loader-message');
        
        if (show) {
            if (!loader) {
                loader = document.createElement('div');
                loader.className = 'loader-message';
                loader.innerHTML = `
                    <div class="loading-spinner"></div>
                    <p>Caricamento anime in corso...</p>
                `;
                section.querySelector('.anime-container').innerHTML = '';
                section.querySelector('.anime-container').appendChild(loader);
            }
        } else if (loader) {
            loader.remove();
        }
    }

    // Funzione per popolare una sezione
    async function populateSection(endpoint, containerId, isCalendar = false) {
        try {
            console.log(`Fetching data from ${endpoint}`); // Debug log
            const response = await fetch(endpoint);
            const data = await response.json();
            console.log(`Data received from ${endpoint}:`, data); // Debug log
            
            const container = document.getElementById(containerId);
            if (!container) {
                console.error(`Container ${containerId} not found`);
                return;
            }
            
            // Pulisci il contenitore prima di aggiungere nuove card
            container.innerHTML = '';
            
            if (isCalendar && data.anime) {
                data.anime.forEach(anime => {
                    container.appendChild(createAnimeCard(anime, true));
                });
            } else if (Array.isArray(data)) {
                data.forEach(anime => {
                    container.appendChild(createAnimeCard(anime));
                });
            } else {
                console.error(`Invalid data format from ${endpoint}`);
            }
        } catch (error) {
            console.error(`Error loading ${endpoint}:`, error);
        }
    }

    // Modifica le funzioni di fetch per includere il loader
    async function fetchPopolari() {
        toggleLoader('#popolari', true);
        try {
            const response = await fetch('/api/popolari');
            const data = await response.json();
            const container = document.querySelector('#popolari .anime-container');
            container.innerHTML = '';
            data.forEach(anime => {
                container.appendChild(createAnimeCard(anime));
            });
        } catch (error) {
            console.error('Errore nel caricamento degli anime popolari:', error);
        } finally {
            toggleLoader('#popolari', false);
        }
    }

    // Applica lo stesso pattern alle altre funzioni
    async function fetchUltimeUscite() {
        toggleLoader('#ultime-uscite', true);
        try {
            const response = await fetch('/api/ultime-uscite');
            const data = await response.json();
            const container = document.querySelector('#ultime-uscite .anime-container');
            container.innerHTML = '';
            data.forEach(anime => {
                container.appendChild(createAnimeCard(anime));
            });
        } catch (error) {
            console.error('Errore nel caricamento delle ultime uscite:', error);
        } finally {
            toggleLoader('#ultime-uscite', false);
        }
    }

    async function fetchUltimiEpisodi() {
        toggleLoader('#ultimi-episodi', true);
        try {
            const response = await fetch('/api/ultimi-episodi');
            const data = await response.json();
            const container = document.querySelector('#ultimi-episodi .anime-container');
            container.innerHTML = '';
            data.forEach(anime => {
                container.appendChild(createAnimeCard(anime));
            });
        } catch (error) {
            console.error('Errore nel caricamento degli ultimi episodi:', error);
        } finally {
            toggleLoader('#ultimi-episodi', false);
        }
    }

    // Popola tutte le sezioni
    populateSection('/api/popolari', 'popolari');
    populateSection('/api/ultime-uscite', 'ultime-uscite');
    populateSection('/api/calendario', 'calendario', true);
    populateSection('/api/ultimi-episodi', 'ultimi-episodi');

    // Gestione dei pulsanti di scroll
    const scrollContainers = document.querySelectorAll('.scroll-container');
    
    scrollContainers.forEach(container => {
        const list = container.querySelector('.anime-list');
        const leftButton = container.querySelector('.scroll-button.left');
        const rightButton = container.querySelector('.scroll-button.right');

        if (leftButton && rightButton) {
            leftButton.addEventListener('click', () => {
                list.scrollBy({
                    left: -300,
                    behavior: 'smooth'
                });
            });

            rightButton.addEventListener('click', () => {
                list.scrollBy({
                    left: 300,
                    behavior: 'smooth'
                });
            });
        }
    });
});
