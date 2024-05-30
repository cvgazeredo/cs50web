document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_mail);
  //document.querySelector('#view-email').addEventListener('click', view_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

//3- View Email
function view_email(email_id) {

  //Show email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';
  

  console.log(email_id)

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email)
    const email_element = document.createElement('div');
    email_element.innerHTML = `
      <h5>From: ${email.sender}</h5>
      <h5>To: ${email.recipients}</h5>
      <h5>Subject: ${email.subject}</h5>
      <h6>${email.timestamp}</h6>
      <p>${email.body}</p>
    `;
    document.querySelector('#view-email').innerHTML = "";
    document.querySelector('#view-email').append(email_element);

    const reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply";
      
      reply_button.addEventListener('click', function() {
        compose_email();

        document.querySelector('#compose-recipients').value = `${email.sender}`;
        document.querySelector('#compose-subject').value = "Re: " + `${email.subject}`;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.recipients} wrote: \n\n${email.body}`;
        
      })
      document.querySelector('#view-email').append(reply_button);

  })
}

function readed_email(email_id) {

    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
    console.log("This email has been marked as READED!")
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  console.log("MAILBOX => " + mailbox)


  //2- MailBox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    
    emails.forEach(email => {
      const sender = email.sender
      const subject = email.subject
      const timestamp = email.timestamp
      const email_id = email.id
      const archive = email.archived
      console.log(archive)

      const element = document.createElement('div');
      element.className = "list-group-item";
      element.className = email.read ? 'read': 'unread';
      //element.innerHTML = email.archived ? "read" : "unread";
      
      element.innerHTML = `
      <h5>From: ${sender}</h5>
      <h5>${subject}</h5>
      <h7>Timestamp: ${timestamp}</h7>
      `;
      
      element.addEventListener('click', function() {
        view_email(email_id), readed_email(email_id)
      });
      document.querySelector('#emails-view').append(element);

      const button = document.createElement('button');
      //condition ? exprIfTrue : expreIfFalse
      button.innerHTML = email.archived ? "Unarchive" : "Archive";
      button.className = email.archived ? "btn btn-success" : "btn btn-danger"
      button.addEventListener('click', function() {

        //4-Archive and Unarchive
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
        .then( () => {
          load_mailbox('inbox')
        })
      });
      document.querySelector('#emails-view').append(button);

    })     
 });
 
}


// 1 - Send Mail
function send_mail(event) {
    
    event.preventDefault()

    const recipients = document.querySelector('#compose-recipients').value
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value


    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body  
      })
    })
    .then(response => response.json())
    .then(result => {
      load_mailbox('sent')
    })
}


