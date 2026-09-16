const API_URL = "https://futpredict-4ei2.onrender.com/api";

document.addEventListener("DOMContentLoaded", () => {
    loadMatches();
});

async function loadMatches() {
    const matchesList = document.getElementById("matches-list");
    if (!matchesList) return;

    try {
        const response = await fetch(`${API_URL}/matches/`);
        const matches = await response.json();

        let headerHTML = `
            <div style="margin-bottom: 20px; text-align: center;">
                <button onclick="syncLiveMatches()" style="padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
                    🔄 Sincronizar Fixture de Argentina
                </button>
                <p id="sync-status" style="margin-top: 8px; font-size: 0.9em; color: #aaa;"></p>
            </div>
        `;

        if (matches.length === 0) {
            matchesList.innerHTML = headerHTML + "<p>No hay partidos registrados. Haz clic en Sincronizar.</p>";
            return;
        }

        matchesList.innerHTML = headerHTML + matches.map(match => `
            <div class="match-card" style="border: 1px solid #333; padding: 15px; margin-bottom: 15px; border-radius: 8px; background: #1e1e2e; color: #fff;">
                <h3>${match.home_team} vs ${match.away_team}</h3>
                <p><strong>Estado:</strong> ${match.status}</p>
                <button onclick="generatePrediction(${match.id})" style="padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Generar Predicción
                </button>
                <div id="prediction-${match.id}"></div>
            </div>
        `).join('');
    } catch (error) {
        console.error("Error al cargar partidos:", error);
        matchesList.innerHTML = "<p>Error al conectar con el servidor.</p>";
    }
}

async function syncLiveMatches() {
    const statusEl = document.getElementById("sync-status");
    if (statusEl) statusEl.innerText = "Consultando fixture en la API...";

    try {
        const response = await fetch(`${API_URL}/matches/sync`, { method: 'POST' });
        const data = await response.json();
        
        if (response.ok) {
            if (statusEl) statusEl.innerText = data.message;
            setTimeout(() => loadMatches(), 1000);
        } else {
            if (statusEl) statusEl.innerText = data.detail || "Error al sincronizar.";
        }
    } catch (error) {
        console.error("Error al sincronizar:", error);
        if (statusEl) statusEl.innerText = "Error de conexión con el servidor.";
    }
}

async function generatePrediction(matchId) {
    const resultContainer = document.getElementById(`prediction-${matchId}`);
    if (resultContainer) resultContainer.innerText = "Calculando...";

    try {
        const response = await fetch(`${API_URL}/predictions/generate/${matchId}`, {
            method: 'POST'
        });
        const data = await response.json();

        if (resultContainer) {
            resultContainer.innerHTML = `
                <div style="margin-top: 10px; padding: 10px; background: rgba(255, 255, 255, 0.08); border-radius: 6px;">
                    <p><strong>Pronóstico:</strong> ${data.predicted_winner}</p>
                    <p><strong>Confianza:</strong> ${(data.confidence * 100).toFixed(0)}%</p>
                    <p><strong>Goles por Equipo:</strong> ${data.home_exp_goals} - ${data.away_exp_goals}</p>
                    <p><strong>Total de Goles Esperados:</strong> ${data.total_exp_goals}</p>
                    <p><strong>Total de Córners Esperados:</strong> 🚩 ${data.total_exp_corners}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error("Error al generar la predicción:", error);
        if (resultContainer) resultContainer.innerText = "Error al calcular predicción.";
    }
}