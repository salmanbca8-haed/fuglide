/**
 * FU-GLIDE | Form Processing, Firebase Firestore & Instant WhatsApp/Email Dispatch
 */

const formMessage = document.getElementById('formMessage');
const EMAIL_RECIPIENT = 'salmanbca8@gmail.com';
const WHATSAPP_NUMBER = '9629255773';

function showMessage(message, isError = false) {
  if (!formMessage) return;
  formMessage.textContent = message;
  formMessage.style.color = isError ? '#ff4d4d' : 'var(--secondary)';
  formMessage.style.textShadow = isError ? '0 0 10px rgba(255, 77, 77, 0.4)' : '0 0 10px var(--secondary-glow)';
  formMessage.style.opacity = '1';
  
  if (message) {
    formMessage.animate([
      { opacity: 0, transform: 'translateY(6px)' },
      { opacity: 1, transform: 'translateY(0)' }
    ], {
      duration: 300,
      easing: 'ease-out'
    });
  }
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePhone(phone) {
  return /^[0-9\s+-]{7,20}$/.test(phone);
}

function createMailToUrl(subject, body) {
  return `mailto:${EMAIL_RECIPIENT}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

function openExternalUrl(url) {
  if (url.startsWith('mailto:')) {
    window.location.href = url;
    return;
  }

  const popup = window.open(url, '_blank', 'noopener,noreferrer');

  if (!popup) {
    const helperLink = document.createElement('a');
    helperLink.href = url;
    helperLink.target = '_blank';
    helperLink.rel = 'noopener noreferrer';
    helperLink.style.display = 'none';
    document.body.appendChild(helperLink);
    helperLink.click();
    helperLink.remove();
  }
}

function createWhatsAppUrl(phone, text) {
  const cleaned = phone.replace(/[^0-9]/g, '');
  return `https://wa.me/${cleaned}?text=${encodeURIComponent(text)}`;
}

function buildNotificationText(title, fields, values) {
  const submittedAt = new Date().toLocaleString();
  const content = fields
    .map((field) => `${field.label}: ${values[field.id] || ''}`)
    .join('\n');
  return `${title} Submission\nSubmitted: ${submittedAt}\n\n${content}`;
}

async function saveDocument(collectionName, payload) {
  if (typeof db === 'undefined' || !db || !db.collection) return;
  return db.collection(collectionName).add(payload);
}

function setLoading(button, isLoading) {
  if (!button) return;
  button.disabled = isLoading;
  button.textContent = isLoading ? 'Submitting...' : button.dataset.originalText || button.textContent;
  if (isLoading) {
    button.style.opacity = '0.85';
  } else {
    button.style.opacity = '1';
  }
}

function dispatchNotifications(title, fields, values) {
  const text = buildNotificationText(title, fields, values);
  const whatsappUrl = createWhatsAppUrl(WHATSAPP_NUMBER, text);
  const mailtoUrl = createMailToUrl(`${title} Submission`, text);

  openExternalUrl(whatsappUrl);
  openExternalUrl(mailtoUrl);
}

function dispatchEmailOnly(title, fields, values) {
  const text = buildNotificationText(title, fields, values);
  const mailtoUrl = createMailToUrl(`${title} Submission`, text);

  openExternalUrl(mailtoUrl);
}

function attachFormHandler(formId, collectionName, fields, title) {
  const form = document.getElementById(formId);
  if (!form) return;

  const submitButton = form.querySelector('button[type="submit"]');
  const emailButton = form.querySelector('.email-action');

  if (submitButton) {
    submitButton.dataset.originalText = submitButton.textContent;
  }

  if (emailButton) {
    emailButton.addEventListener('click', () => {
      const values = {};
      let valid = true;

      for (const field of fields) {
        const input = form.querySelector(`#${field.id}`);
        if (!input) continue;

        const value = field.getValue ? field.getValue(input) : input.value.trim();
        values[field.id] = value;

        if (field.required && !value) {
          valid = false;
          input.focus();
          showMessage(`${field.label} is required.`, true);
          break;
        }

        if (field.type === 'email' && value && !validateEmail(value)) {
          valid = false;
          input.focus();
          showMessage('Please enter a valid email address.', true);
          break;
        }

        if (field.type === 'phone' && value && !validatePhone(value)) {
          valid = false;
          input.focus();
          showMessage('Please enter a valid phone number.', true);
          break;
        }
      }

      if (!valid) return;
      dispatchEmailOnly(title, fields, values);
      showMessage('Opening your email client with the current details...');
    });
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    showMessage('');

    const values = {};
    let valid = true;

    for (const field of fields) {
      const input = form.querySelector(`#${field.id}`);
      if (!input) continue;

      const value = field.getValue ? field.getValue(input) : input.value.trim();
      values[field.id] = value;

      if (field.required && !value) {
        valid = false;
        input.focus();
        showMessage(`${field.label} is required.`, true);
        break;
      }

      if (field.type === 'email' && value && !validateEmail(value)) {
        valid = false;
        input.focus();
        showMessage('Please enter a valid email address.', true);
        break;
      }

      if (field.type === 'phone' && value && !validatePhone(value)) {
        valid = false;
        input.focus();
        showMessage('Please enter a valid phone number.', true);
        break;
      }
    }

    if (!valid) return;

    setLoading(submitButton, true);

    const notificationFields = fields;
    const notificationValues = { ...values };

    try {
      dispatchNotifications(title, notificationFields, notificationValues);
      const submittedAt = new Date().toISOString();
      saveDocument(collectionName, { ...values, createdAt: submittedAt, submittedAt }).catch((error) => {
        console.error('Save failed:', error);
      });
      form.reset();
      showMessage('Thanks! Your message has been sent and shared via WhatsApp.');
    } catch (error) {
      console.error(error);
      showMessage('Something went wrong. Please try again later.', true);
    } finally {
      setLoading(submitButton, false);
    }
  });
}

attachFormHandler(
  'applicationForm',
  'applications',
  [
    { id: 'name', label: 'Name', required: true },
    { id: 'email', label: 'Email', required: true, type: 'email' },
    { id: 'phone', label: 'Phone', required: true, type: 'phone' },
    { id: 'course', label: 'Course', required: true },
    { id: 'batch', label: 'Preferred batch time', required: true },
    { id: 'qualifications', label: 'Qualifications', required: true },
    {
      id: 'document',
      required: false,
      getValue: (input) => (input.files && input.files[0] ? input.files[0].name : 'None'),
    },
  ],
  'Application'
);

attachFormHandler(
  'contactForm',
  'contactMessages',
  [
    { id: 'name', label: 'Name', required: true },
    { id: 'email', label: 'Email', required: true, type: 'email' },
    { id: 'subject', label: 'Subject', required: true },
    { id: 'message', label: 'Message', required: true },
  ],
  'Contact'
);
