// mattoquiz/assets/js/quiz.js

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".mattoquiz").forEach(initQuiz);
});

function initQuiz(wrapper) {
    const quizId = wrapper.dataset.quizId;
    const container = wrapper.querySelector(`#mattoquiz-container-${quizId}`);
    const dataUrl = `/index.php?rex-api-call=mattoquiz&type=api&quizId=${quizId}`;

    fetch(dataUrl)
        .then((res) => res.json())
        .then((quiz) => renderQuiz(wrapper, container, quiz));
}

/* ---------------------------------------------------------
   Fortschrittskreis – animierte Variante
--------------------------------------------------------- */
function updateProgress(current, total) {
    const percent = (current / total) * 100;
    const circle = document.querySelector(".mattoquiz-progress .fg");
    const text = document.querySelector(".mattoquiz-progress .progress-text");
    const currentLabel = document.getElementById("current-question");
    const totalLabel = document.getElementById("total-questions");

    if (circle) {
        const currentOffset = parseFloat(circle.dataset.offset || 100);
        const targetOffset = 100 - percent;
        const start = performance.now();
        const duration = 600;

        function animate(time) {
            const progress = Math.min((time - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
            const offset = currentOffset + (targetOffset - currentOffset) * eased;
            circle.style.strokeDashoffset = offset;
            if (progress < 1) requestAnimationFrame(animate);
            else circle.dataset.offset = targetOffset;
        }
        requestAnimationFrame(animate);
    }

    if (text) text.textContent = `${current}/${total}`;
    if (currentLabel) currentLabel.textContent = current;
    if (totalLabel) totalLabel.textContent = total;
}

/* ---------------------------------------------------------
   Haupt-Renderer
--------------------------------------------------------- */
function renderQuiz(wrapper, container, quiz) {
    let index = 0;
    let correctCount = 0;
    const total = quiz.questions.length;

    const renderQuestion = () => {
        const q = quiz.questions[index];

        container.innerHTML = `
      <div class="mattoquiz-progress">
        <div class="progress-circle" data-progress="0">
          <svg>
            <circle class="bg" cx="24" cy="24" r="22"></circle>
            <circle class="fg" cx="24" cy="24" r="22" data-offset="100"></circle>
          </svg>
          <span class="progress-text">${index + 1}/${total}</span>
        </div>
        <div class="progress-label">Frage <span id="current-question">${index + 1}</span> von <span id="total-questions">${total}</span></div>
      </div>

      <div class="quiz-question"><h2>${q.question}</h2></div>
      <div class="row g-3">
        ${["a", "b", "c", "d"]
            .map(
                (letter) => `
          <div class="col-6">
            <div class="card quiz-answer" data-letter="${letter.toUpperCase()}">
              <div class="card-body">${q["answer_" + letter]}</div>
            </div>
          </div>`
            )
            .join("")}
      </div>
      <div class="quiz-explanation alert alert-info mt-3" style="display:none;">${q.explanation}</div>
    `;

        updateProgress(index + 1, total); // 🚀 Fortschritt aktualisieren

        const answers = container.querySelectorAll(".quiz-answer");
        answers.forEach((el) => el.addEventListener("click", () => handleAnswer(el, q)));
    };

    const handleAnswer = (el, q) => {
        const chosen = el.dataset.letter;
        const correct = q.correct_answer;

        const allAnswers = container.querySelectorAll(".quiz-answer");
        allAnswers.forEach((a) => {
            a.style.pointerEvents = "none";
            if (a.dataset.letter === correct) a.classList.add("correct");
            if (a.dataset.letter === chosen && chosen !== correct)
                a.classList.add("incorrect");
        });

        const explanation = container.querySelector(".quiz-explanation");
        const feedback = document.createElement("div");
        feedback.className = "quiz-feedback " + (chosen === correct ? "correct" : "incorrect");
        feedback.textContent = chosen === correct ? "Richtig!" : "Falsch!";
        explanation.parentNode.insertBefore(feedback, explanation); // füge Feedback VOR der Erklärung ein
        explanation.style.display = "block";




        if (chosen === correct) correctCount++;

        const nextBtn = document.createElement("button");
        nextBtn.className = "btn btn-secondary mt-3";
        nextBtn.textContent =
            index + 1 === quiz.questions.length
                ? "Ergebnis anzeigen"
                : "Nächste Frage";
        nextBtn.addEventListener("click", () => {
            index++;
            if (index < quiz.questions.length) renderQuestion();
            else renderResult();
        });

        container.appendChild(nextBtn);
    };

    const renderResult = () => {
        const percent = Math.round((correctCount / total) * 100);

        // Ergebnis sofort anzeigen (mit Platzhalter)
        container.innerHTML = `
    <div class="quiz-result text-center text-white">
      <h4>Sie haben ${correctCount} von ${total} Fragen richtig beantwortet!</h4>
      <div class="progress my-3" style="height: 20px;">
        <div class="progress-bar bg-success" style="width: ${percent}%;">
          ${percent}%
        </div>
      </div>

      <p id="quiz-stat-${quiz.id}" class="quiz-stat" aria-live="polite">
        Berechne Vergleich&hellip;
      </p>

      <p>Teilen Sie dieses Quiz:</p>
      <div class="btn-group mb-3">
        <a class="btn btn-info"
           href="mailto:?subject=Quiz%20weiterleiten&body=Schau%20dir%20dieses%20Quiz%20an:%20${encodeURIComponent(window.location.href)}">
           E-Mail
        </a>
        <a class="btn btn-success"
           href="https://wa.me/?text=${encodeURIComponent('Schau dir dieses Quiz an: ' + window.location.href)}"
           target="_blank" rel="noopener">
           WhatsApp
        </a>
        <button class="btn btn-warning" id="copyLinkBtn">Link kopieren</button>
      </div>
      <br>
      <button class="btn btn-secondary" id="restartQuiz">Quiz wiederholen</button>
    </div>
  `;

        // Referenz auf den Platzhalter sichern
        const statEl = document.getElementById(`quiz-stat-${quiz.id}`);

        // Nur loggen, wenn in dieser Session noch nicht geschehen
        if (!sessionStorage.getItem('quiz_logged_' + quiz.id)) {
            fetch('/index.php?rex-api-call=mattoquiz&type=log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    mattoquiz_log: 1,
                    quiz_id: quiz.id,
                    score: percent
                })
            })
                .then(res => res.ok ? res.json() : Promise.reject())
                .then(data => {
                    // Flag erst NACH erfolgreichem Log setzen
                    sessionStorage.setItem('quiz_logged_' + quiz.id, '1');
                    if (statEl) {
                        statEl.innerHTML = `🎯 Sie waren besser als <strong>${data.percentile}%</strong> der Teilnehmer.`;
                    }
                })
                .catch(() => {
                    if (statEl) statEl.textContent = 'Vergleichsdaten derzeit nicht verfügbar.';
                });
        } else {
            // Bereits geloggt – höfliche Info anzeigen
            if (statEl) {
                statEl.textContent = 'Ergebnis gespeichert. Sie waren schon in dieser Sitzung aktiv.';
            }
        }

        // Buttons
        container.querySelector("#restartQuiz").addEventListener("click", () => {
            // Beim Restart erneut loggen erlauben
            sessionStorage.removeItem('quiz_logged_' + quiz.id);
            index = 0;
            correctCount = 0;
            renderQuestion();
        });

        container.querySelector("#copyLinkBtn").addEventListener("click", () => {
            navigator.clipboard.writeText(window.location.href);
            alert("Link kopiert!");
        });
    };


    renderQuestion();
}

