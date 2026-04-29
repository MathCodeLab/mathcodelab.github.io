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
    function renderContact() {
      return `
        <div class="verify-contact">Bei Fragen kontaktieren Sie uns: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></div>
      `;
    }

    if (data.status === 'valid') {
      return `
        <div class="verify-status verified">Zertifikat gültig</div>
        <div class="verify-details-grid">
          ${renderMeta('Student name', data.student_name)}
          ${renderMeta('Course title', data.course_title)}
          ${renderMeta('Abschlussdatum', data.completion_date)}
          ${renderMeta('Dauer', `${data.duration_hours} Stunden`)}
          ${renderMeta('Herausgeber', data.issuer)}
          ${renderMeta('Dozent', data.instructor)}
          ${renderMeta('Zertifikat‑ID', data.certificate_id)}
          ${data.verified_at ? renderMeta('Bestätigt am', data.verified_at) : ''}
        </div>
        <div class="verify-note">Dieses Zertifikat wurde von MathCodeLab ausgestellt. Weitere Informationen unter <a href="https://mathcodelab.de" target="_blank" rel="noreferrer">mathcodelab.de</a>.</div>
        ${renderContact()}
      `;
    } else if (data.status === 'revoked') {
      return `
        <div class="verify-status revoked">Zertifikat widerrufen</div>
        <div class="verify-details-grid">
          ${renderMeta('Zertifikat‑ID', data.certificate_id)}
          ${data.revocation_reason ? renderMeta('Widerrufsgrund', data.revocation_reason) : ''}
        </div>
        <div class="verify-note">Dieses Zertifikat wurde von MathCodeLab widerrufen.</div>
        ${renderContact()}
      `;
    } else {
      return `
        <div class="verify-status invalid">Zertifikat nicht gefunden</div>
        <div class="verify-note verify-note-warn">Es wurde kein Zertifikat mit dieser ID im MathCodeLab-Verifizierungssystem gefunden.</div>
        <div class="verify-suggestion">Vorschläge: Überprüfen Sie das ID‑Format, entfernen Sie Leerzeichen oder versuchen Sie folgendes Beispiel: <strong>MCL-2026-GLMMEO7</strong>.</div>
        <div class="verify-contact">Kontaktieren Sie uns: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></div>
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
      if (!resp.ok) throw new Error('not found');
      const data = await resp.json();
      showResult(renderCertificate(data));
    } catch (err) {
      if (err.message === 'not found') {
        showResult(renderCertificate({status: 'invalid', certificate_id: id}));
      } else {
        showResult('<div class="verify-status invalid">Fehler</div><div class="verify-note verify-note-warn">Der Verifizierungsdienst ist derzeit nicht erreichbar. Kontaktieren Sie uns.</div><div class="verify-contact">Kontakt: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></div>');
      }
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
      showResult(`<div class="verify-status invalid">Ungültiges Format</div><div class="verify-note verify-note-warn">Bitte verwenden Sie das Format <strong>MCL-JJJJ-XXXXXXX</strong>. Beispiel: <strong>MCL-2026-GLMMEO7</strong>.</div><div class="verify-contact">kontaktieren Sie uns: <a href="mailto:info@mathcodelab.de">info@mathcodelab.de</a></div>`);
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
