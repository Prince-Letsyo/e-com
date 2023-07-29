var siteForm = document.querySelector('#create_site')
var websiteDiv = document.querySelector('#website_div')

const create_site = (link = '/auth/create_domain/') => {
  var siteBtn = document.querySelector('#submit_site')
  var domainName = document.querySelector('#domain_name')
  var displayName = document.querySelector('#display_name')

  siteBtn.addEventListener('click', (event) => {
    event.preventDefault()
    const name = displayName.value
    const domain = domainName.value
    fetch(link, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({ name, domain }),
    }).then((data) => {
      if (data.ok)
        data.json().then((d) => {
          websiteDiv.innerHTML = `<div id="website_name" />
              <p><span>Website: </span>${d.name}</p>
              <button id="edit_site">Edit</button> 
              </div>`
          var editSite = document.querySelector('#edit_site')

          site_db_id(editSite)
        })
      else data.json().then((e) => console.log(e))
    })
  })
}
if (siteForm) create_site()

const site_db_id = (editSite = null) => {
  var edit = null
  if (editSite == null) edit = document.querySelector('#edit_site')
  else edit = editSite

  edit.addEventListener('click', (event) => {
    fetch(`/auth/site/`).then((res) => {
      if (res.ok) {
        res.json().then((data) => {
          websiteDiv.innerHTML = `
          <form id="create_site" method="POST">
            <label htmlFor="domain_name">Domain Name</label>
            <input type="text" value="${data.domain}" id="domain_name" placeholder="http://www.example.com" />
            <br />
            <br />
            <label htmlFor="display_name">Display Name</label>
            <input type="text" value="${data.name}" id="display_name" placeholder="www.example.com" />
            <br />
            <br />
            <input type="submit" id="submit_site" />
          </form>`

          create_site((link = `/auth/update_domain/`))
        })
      }
    })
  })
}

site_db_id()
