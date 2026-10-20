/**
 * Builds the "AURORA: register your interest" Google Form and a linked
 * response Sheet in the Google account that runs it.
 *
 * How to run (about 2 minutes):
 *   1. Go to https://script.google.com and choose New project.
 *   2. Replace the editor contents with this file and click Save.
 *   3. Choose buildAuroraForm in the function menu and click Run.
 *      Approve the permissions prompt (Forms and Sheets in your own account).
 *   4. Open View > Logs (or Execution log). Copy the "Respondent link".
 *   5. Paste it into form.json in this repository as "form_url" and push.
 *      The QR code never changes; it points at the registration page.
 *
 * The form collects contact and site details only. Its description tells
 * respondents not to enter any patient information.
 */
function buildAuroraForm() {
  var form = FormApp.create('AURORA: register your interest');
  form.setDescription(
    'AURORA is a research model that reads 2D transabdominal ultrasound for signs of ' +
    'placenta accreta spectrum (PAS). Register here if you would like to use AURORA ' +
    'for research, or if your center would like to help train AURORA 2.0.\n\n' +
    'AURORA is an investigational device and is not for clinical diagnosis. ' +
    'Please do not enter any patient information in this form.'
  );
  form.setConfirmationMessage(
    'Thank you for registering. The AURORA team will contact you as research access ' +
    'and the multicenter consortium open.'
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(false);

  // Contact
  form.addTextItem()
    .setTitle('Name')
    .setRequired(true);

  var emailRule = FormApp.createTextValidation()
    .requireTextIsEmail()
    .setHelpText('Please enter a valid email address.')
    .build();
  form.addTextItem()
    .setTitle('Email')
    .setHelpText('An institutional address helps us verify research access.')
    .setValidation(emailRule)
    .setRequired(true);

  form.addTextItem()
    .setTitle('Institution')
    .setHelpText('Hospital, university or organization.')
    .setRequired(true);

  var role = form.addMultipleChoiceItem().setTitle('Role');
  role.setChoices([
    role.createChoice('Maternal-fetal medicine physician'),
    role.createChoice('Obstetrician-gynecologist'),
    role.createChoice('Radiologist'),
    role.createChoice('Sonographer'),
    role.createChoice('Trainee (fellow or resident)'),
    role.createChoice('Scientist or engineer')
  ]);
  role.showOtherOption(true).setRequired(true);

  form.addTextItem()
    .setTitle('Country')
    .setRequired(true);

  // Interest
  var interest = form.addCheckboxItem().setTitle('What are you interested in?');
  interest.setChoices([
    interest.createChoice('Using AURORA for research on scans at my institution'),
    interest.createChoice('Contributing de-identified ultrasound images to train AURORA 2.0')
  ]);
  interest.setRequired(true);

  var multi = form.addMultipleChoiceItem().setTitle('Are you interested in a multicenter collaboration?');
  multi.setChoices([
    multi.createChoice('Yes'),
    multi.createChoice('Maybe, tell me more'),
    multi.createChoice('No')
  ]);
  multi.setRequired(true);

  // Site details
  form.addTextItem()
    .setTitle('Ultrasound machine(s) used')
    .setHelpText('Manufacturer and model, for example GE Voluson E10. List all that apply.')
    .setRequired(true);

  form.addTextItem()
    .setTitle('Ultrasound interpretation or reporting software')
    .setHelpText('The reporting system, viewer or PACS your unit uses to read obstetric scans.')
    .setRequired(false);

  var countRule = FormApp.createTextValidation()
    .requireNumberGreaterThanOrEqualTo(0)
    .setHelpText('Please enter a number. An estimate is fine.')
    .build();
  form.addTextItem()
    .setTitle('Number of PAS cases per year at your center')
    .setHelpText('Approximate number of placenta accreta spectrum deliveries per year.')
    .setValidation(countRule)
    .setRequired(true);

  var pathology = form.addMultipleChoiceItem()
    .setTitle('Are PAS cases at your center confirmed by histopathology?');
  pathology.setChoices([
    pathology.createChoice('Yes, routinely'),
    pathology.createChoice('Sometimes'),
    pathology.createChoice('No'),
    pathology.createChoice('Not sure')
  ]);
  pathology.setRequired(true);

  // Consent
  var consent = form.addCheckboxItem()
    .setTitle('Contact consent')
    .setHelpText(
      'Your answers are stored in a Google Sheet that only the AURORA team can open. ' +
      'We use them only to contact you about AURORA and to plan the consortium. ' +
      'We do not share or sell them. Ask us at any time to delete your entry.'
    );
  consent.setChoices([
    consent.createChoice('I agree that the AURORA team may contact me about AURORA using the details above.')
  ]);
  consent.setRequired(true);

  // Responses go to a new Sheet in the same account.
  var sheet = SpreadsheetApp.create('AURORA interest registrations (responses)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());

  var respondentLink = form.getPublishedUrl();
  Logger.log('Respondent link (paste into form.json): ' + respondentLink);
  Logger.log('Short link: ' + form.shortenFormUrl(respondentLink));
  Logger.log('Edit link (keep private): ' + form.getEditUrl());
  Logger.log('Response sheet (keep private): ' + sheet.getUrl());
}
