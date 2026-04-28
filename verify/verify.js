// MathCodeLab Certificate Verification Frontend
(function() {
  const API_BASE = 'https://api.mathcodelab.de';
  const mainContent = document.getElementById('main-content');
  const loadingDiv = document.getElementById('loading');
  const resultDiv = document.getElementById('result');
  const searchForm = document.getElementById('search-form');
  const yearSpan = document.getElementById('year');
  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  function getCertificateIdFromUrl() {
    // Support /verify/?id=... and /verify/ID
    const url = new URL(window.location.href);
    let id = url.searchParams.get('id');
    if (!id) {
      // Try to extract from path
      const pathParts = url.pathname.split('/').filter(Boolean);
      const verifyIdx = pathParts.indexOf('verify');
      if (verifyIdx !== -1 && pathParts.length > verifyIdx + 1) {
        id = pathParts[verifyIdx + 1];
      }
    }
    return id;
  }

  function showLoading(show) {
    loadingDiv.classList.toggle('hidden', !show);
    resultDiv.innerHTML = '';
    searchForm.classList.add('hidden');
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
  }

  function renderCertificate(data) {
    if (data.status === 'valid') {
      return `
        <div class="status verified">Verified Certificate</div>
        <dl class="certificate-details">
          <dt>Student Name</dt><dd>${escapeHtml(data.student_name)}</dd>
          <dt>Course Title</dt><dd>${escapeHtml(data.course_title)}</dd>
          <dt>Completion Date</dt><dd>${escapeHtml(data.completion_date)}</dd>
          <dt>Duration</dt><dd>${escapeHtml(data.duration_hours)} hours</dd>
          <dt>Issuer</dt><dd>${escapeHtml(data.issuer)}</dd>
          <dt>Instructor</dt><dd>${escapeHtml(data.instructor)}</dd>
          <dt>Certificate ID</dt><dd>${escapeHtml(data.certificate_id)}</dd>
          <dt>Verified At</dt><dd>${escapeHtml(data.verified_at)}</dd>
        </dl>
        <div class="note">This certificate was issued by MathCodeLab. For more information, visit <a href="https://mathcodelab.de" target="_blank">mathcodelab.de</a>.</div>
      `;
    } else if (data.status === 'revoked') {
      return `
        <div class="status revoked">Certificate Revoked</div>
        <dl class="certificate-details">
          <dt>Certificate ID</dt><dd>${escapeHtml(data.certificate_id)}</dd>
          ${data.revocation_reason ? `<dt>Revocation Reason</dt><dd>${escapeHtml(data.revocation_reason)}</dd>` : ''}
        </dl>
        <div class="note">This certificate was revoked by MathCodeLab.</div>
      `;
    } else {
      return `
        <div class="status invalid">Certificate Not Found</div>
        <div class="certificate-details">
          <p>No certificate with this ID was found in the MathCodeLab verification system.</p>
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
        showResult('<div class="status invalid">Error</div><div class="certificate-details"><p>Could not reach the verification server. Please try again later.</p></div>');
      }
    }
  }

  // Handle form submit
  searchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const id = document.getElementById('certificate-id').value.trim();
    if (id) verifyCertificate(id);
  });

  // Main logic
  const certId = getCertificateIdFromUrl();
  if (certId) {
    verifyCertificate(certId);
  } else {
    showSearchForm();
  }
})();
