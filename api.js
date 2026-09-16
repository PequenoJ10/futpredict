const API_URL = "https://futpredict-4ei2.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
    loadMatches();
});

async function loadMatches() {
    const matchesList = document.getElementById("matches-container") || document.getElementById("matches-list");
    if (!matchesList) return;

    try {
        const response = await fetch(`${API_URL}/api/matches/`);
        if (!response.ok) throw new Error("No se pudieron cargar los partidos");
        
        const matches = await response.json();

        if (!matches || matches.length === 0) {
            matchesList.innerHTML = "<p style='color: #aaa;'>No hay partidos registrados. Haz clic en Sincronizar.</p>";
            return;
        }

        matchesList.innerHTML = matches.map((match, index) => {
            const home = match.home_team;
            const away = match.away_team;
            const dateFormatted = new Date(match.match_date || match.date).toLocaleString();

            return `
                <div class="match-card" style="border: 1px solid #333; padding: 15px; margin-bottom: 15px; border-radius: 8px; background: #1e1e2e; color: #fff; text-align: left;">
                    <div style="font-size: 0.75rem; color: #aaa; margin-bottom: 5px;">📅 ${dateFormatted} | Estado: ${match.status}</div>
                    <h3 style="margin: 5px 0 15px 0; text-align: center;">${home} vs ${away}</h3>
                    <button onclick="generatePrediction('${home}', '${away}', ${index})" style="width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;">
                        Generar Predicción
                    </button>
                    <div id="prediction-${index}"></div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error("Error al cargar partidos:", error);
        matchesList.innerHTML = "<p style='color: #ef4444; text-align: center;'>Error conectando con el servidor. (Si Render estaba durmiendo, recarga en 30 segundos).</p>";
    }
}

async function syncMatches() {
    try {
        const res = await fetch(`${API_URL}/api/matches/sync?league_code=PD`, { method: 'POST' });
        if (!res.ok) throw new Error("Error al sincronizar");
        alert("¡Partidos sincronizados con éxito!");
        loadMatches();
    } catch (err) {
        console.error(err);
        alert("Error al sincronizar partidos con el servidor.");
    }
}

async function generatePrediction(home, away, index) {
    const container = document.getElementById(`prediction-${index}`);
    if (container) container.innerHTML = `<p style="text-align:center; color:#38bdf8; margin-top:10px;">Calculando modelo de Poisson...</p>`;

    try {
        const response = await fetch(`${API_URL}/predictions/?home_team=${encodeURIComponent(home)}&away_team=${encodeURIComponent(away)}`, {
            method: 'POST'
        });

        if (!response.ok) throw new Error("Error en el cálculo");

        const data = await response.json();

        if (container) {
            container.innerHTML = `
                <div style="margin-top: 10px; padding: 12px; background: rgba(255, 255, 255, 0.08); border-radius: 6px; font-size: 0.85rem;">
                    <p style="color: #4ade80; font-weight: bold; margin-top:0;">🎯 ${data.prediction}</p>
                    <p style="margin: 5px 0;"><strong>Goles Esperados (xG):</strong> ${data.expected_home_goals} - ${data.expected_away_goals}</p>
                    <p style="margin: 0; color: #aaa;">Probabilidades: Local (${data.home_win_probability}%) | Empate (${data.draw_probability}%) | Visita (${data.away_win_probability}%)</p>
                </div>
            `;
        }
    } catch (error) {
        console.error("Error al generar la predicción:", error);
        if (container) container.innerHTML = `<p style="color: #ef4444; margin-top:10px;">Error al calcular la predicción.</p>`;
    }
}