// MathCodeLab Certificate Verification Frontend
(function() {
  const API_BASE = 'https://api.mathcodelab.de';
  const mainContent = document.getElementById('main-content');
  const loadingDiv = document.getElementById('loading');
  const resultDiv = document.getElementById('result');
  const searchForm = document.getElementById('search-form');
  const certificateInput = document.getElementById('certificate-id');
  const searchButton = searchForm ? searchForm.querySelector('button[type="submit"]') : null;
  const verifyCheckButton = document.getElementById('verify-check');
  const yearSpan = document.getElementById('year');
  const CERT_PATTERN = /^MCL-\d{4}-[A-Z0-9]{6,8}$/;
  let isVerifying = false;
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  function getCertificateIdFromUrl() {
    const url = new URL(window.location.href);
    const certPattern = CERT_PATTERN;

    let id = url.searchParams.get('id');

    if (!id) {
      const pathParts = url.pathname.split('/').filter(Boolean);
      const verifyIdx = pathParts.indexOf('verify');

      if (verifyIdx !== -1 && pathParts.length > verifyIdx + 1) {
        id = pathParts[verifyIdx + 1];
      }
    }

    return certPattern.test(id) ? id : null;
  }

  function showLoading(show) {
    loadingDiv.classList.toggle('hidden', !show);
    resultDiv.innerHTML = '';
    searchForm.classList.add('hidden');
  }

  function setFormBusy(isBusy) {
    isVerifying = isBusy;

    if (certificateInput) {
      certificateInput.disabled = isBusy;
    }

    if (searchButton) {
      searchButton.disabled = isBusy;
      searchButton.textContent = isBusy ? 'Prüfe...' : 'Zertifikat prüfen';
    }

    if (verifyCheckButton) {
      verifyCheckButton.disabled = isBusy;
      verifyCheckButton.textContent = isBusy ? 'Prüfe...' : 'Prüfen';
    }
  }

  function showSearchForm() {
    searchForm.classList.remove('hidden');
    loadingDiv.classList.add('hidden');
    resultDiv.innerHTML = '';
  }

  function showResult(html) {
    loadingDiv.classList.add('hidden');
    searchForm.classList.add('hidden');
    resultDiv.innerHTML = html;
    // attach actions for dynamic result buttons (retry, etc.)
    attachResultActions();
  }

  function attachResultActions() {
    const retryBtn = document.getElementById('retry-btn');
    if (retryBtn) {
      retryBtn.addEventListener('click', function() {
        resultDiv.innerHTML = '';
        showSearchForm();
        certificateInput.focus();
      });
    }
  }

  function renderMeta(title, value) {
    return `
      <div class="verify-meta-item">
        <span class="verify-meta-label">${escapeHtml(title)}</span>
        <span class="verify-meta-value">${escapeHtml(value)}</span>
      </div>
    `;
  }

  function renderCertificate(data) {
    function renderContactLine() {
      return `<p class="verify-contact">Bei Rückfragen kann folgende Adresse kontaktiert werden: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></p>`;
    }

    function formatDateTime(iso) {
      try {
        const d = new Date(iso);
        const dd = String(d.getUTCDate()).padStart(2, '0');
        const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
        const yyyy = d.getUTCFullYear();
        const hh = String(d.getUTCHours()).padStart(2, '0');
        const min = String(d.getUTCMinutes()).padStart(2, '0');
        return `${dd}.${mm}.${yyyy}, ${hh}:${min} UTC`;
      } catch (e) {
        return iso;
      }
    }

    if (data.status === 'valid') {
      const verifiedAt = data.verified_at ? formatDateTime(data.verified_at) : '';
      return `
        <div class="verify-result-card verify-result-success">
          <div class="verify-result-header success">
            <span class="verify-result-badge">Verifiziert</span>
            <h3 class="verify-result-title">Verifiziertes Zertifikat</h3>
            <p class="verify-result-description">Dieses Zertifikat wurde erfolgreich geprüft und als gültig bestätigt.</p>
          </div>
          <div class="verify-details-grid">
            ${renderMeta('Teilnehmer', data.student_name || '-')}
            ${renderMeta('Kurs', data.course_title || '-')}
            ${renderMeta('Abschlussdatum', data.completion_date || '-')}
            ${renderMeta('Dauer', (data.duration_hours != null) ? `${data.duration_hours} Unterrichtsstunden` : '-')}
            ${renderMeta('Herausgeber', data.issuer || 'MathCodeLab')}
            ${renderMeta('Dozent', data.instructor || 'Mohammad Orabe')}
            ${renderMeta('Zertifikat-ID', data.certificate_id)}
            ${verifiedAt ? renderMeta('Verifiziert am', verifiedAt) : ''}
          </div>
          <div class="verify-note">Hinweis:\nDieses Zertifikat bestätigt die erfolgreiche Teilnahme bzw. den Abschluss eines von MathCodeLab durchgeführten Kurses. Es stellt keinen akademischen Abschluss dar und beinhaltet keine Vergabe von Leistungspunkten (ECTS). Eine mögliche Anerkennung durch Dritten erfolgt ausschließlich im Ermessen der jeweiligen Institution.<br>Weitere Informationen sind unter <a href="https://mathcodelab.de" target="_blank" rel="noreferrer">https://mathcodelab.de</a> verfügbar.</div>
          <div class="verify-result-footer">${renderContactLine()}</div>
        </div>
      `;
    } else {
      return `
        <div class="verify-result-card verify-result-invalid">
          <div class="verify-result-header danger">
            <span class="verify-result-badge">Nicht gefunden</span>
            <h3 class="verify-result-title">Zertifikat nicht gefunden</h3>
            <p class="verify-result-description">Zu der angegebenen Zertifikat-ID konnte kein Eintrag in der MathCodeLab-Zertifikatsdatenbank gefunden werden. Es wird gebeten, die eingegebene ID zu überprüfen und erneut einzugeben.</p>
          </div>
          <div class="verify-result-footer">${renderContactLine()}</div>
        </div>
      `;
    }
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function(tag) {
      const chars = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      };
      return chars[tag] || tag;
    });
  }

  async function verifyCertificate(id) {
    if (isVerifying) {
      return;
    }

    setFormBusy(true);
    showLoading(true);
    try {
      const resp = await fetch(`${API_BASE}/verify/${encodeURIComponent(id)}`);
      if (resp.status === 404) {
        showResult(renderCertificate({status: 'invalid', certificate_id: id}));
        return;
      }
      if (!resp.ok) {
        throw new Error('server');
      }
      const data = await resp.json();
      // ensure status field
      data.status = data.status || 'valid';
      showResult(renderCertificate(data));
    } catch (err) {
      // server / network errors -> show server error card
      showResult(`
        <div class="verify-result-card verify-result-invalid">
          <div class="verify-result-header danger">
            <span class="verify-result-badge">Fehler</span>
            <h3 class="verify-result-title">Fehler bei der Verifizierung</h3>
            <p class="verify-result-description">Der Verifizierungsdienst ist derzeit vorübergehend nicht erreichbar. Es wird gebeten, die Anfrage zu einem späteren Zeitpunkt erneut durchzuführen. Sollte das Problem weiterhin bestehen, kann der Support kontaktiert werden.</p>
          </div>
          <div class="verify-result-footer"><p class="verify-contact">Kontakt: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></p></div>
        </div>
      `);
    } finally {
      setFormBusy(false);
    }
  }

  // Handle form submit
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    if (isVerifying) {
      return;
    }

    const id = document.getElementById('certificate-id').value.trim();
    if (!id) return;
    if (!CERT_PATTERN.test(id)) {
      showResult(`
        <div class="verify-result-card verify-result-invalid">
          <div class="verify-result-header danger">
            <span class="verify-result-badge">Ungültige Eingabe</span>
            <h3 class="verify-result-title">Ungültige Eingabe</h3>
            <p class="verify-result-description">Die eingegebene Zertifikat-ID entspricht nicht dem erwarteten Format. Es wird gebeten, folgendes Format zu verwenden: <strong>MCL-JJJJ-XXXXXXX</strong></p>
          </div>
          <div class="verify-suggestion">Beispiel: <strong>MCL-2026-GLMMEO7</strong></div>
          <div class="verify-result-footer"><p class="verify-contact">Bei Rückfragen kann folgende Adresse kontaktiert werden: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></p></div>
        </div>
      `);
      return;
    }
    verifyCertificate(id);
  });

  // Inline check button handler (useful for users who don't press Enter)
  if (verifyCheckButton) {
    // initialize state
    verifyCheckButton.disabled = true;

    verifyCheckButton.addEventListener('click', function() {
      if (isVerifying) return;
      const id = certificateInput.value.trim();
      if (!id) return;
      if (!CERT_PATTERN.test(id)) {
        showResult(`<div class="verify-status invalid">Ungültiges Format</div><div class="verify-note verify-note-warn">Bitte verwenden Sie das Format <strong>MCL-JJJJ-XXXXXXX</strong>. Beispiel: <strong>MCL-2026-GLMMEO7</strong>.</div><div class="verify-contact">Kontaktieren Sie uns: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></div>`);
        return;
      }
      verifyCertificate(id);
    });

    certificateInput.addEventListener('input', function() {
      verifyCheckButton.disabled = !certificateInput.value.trim();
    });
  }

  // Main logic
  const certId = getCertificateIdFromUrl();
  if (certId) {
    verifyCertificate(certId);
  } else {
    showSearchForm();
  }
})();
