function handle_like(id, post_id) {

  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  //getelementbyid when clicked
  const btn = document.getElementById(id)

  const counter = document.getElementById("count_like_" + post_id)
  const updatedCounter = parseInt(counter.textContent) + 1

  fetch(
    "/handle_like",
    {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        post_id: post_id
      })
    }
  )
    .then(res => res.json())
    .then(
      (result) => {
        // Change class to liked based on the clicked id
        btn.classList.remove('unliked')
        btn.classList.add('liked')
        btn.setAttribute("onclick", 'handle_unlike(this.id, ' + post_id + ')')
        counter.textContent = updatedCounter
        counter.id = "count_unlike_" + post_id
      },
      (error) => {
        console.log(error)
      }
    )
}

function handle_unlike(id, post_id) {

  const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  const btn = document.getElementById(id)
  const counter = document.getElementById("count_unlike_" + post_id)

  const updatedCounter = parseInt(counter.textContent) - 1


  fetch(
    "/handle_unlike",
    {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        post_id: post_id
      })
    }
  )
    .then(res => res.json())
    .then(
      (result) => {
        btn.classList.remove('liked')
        btn.classList.add('unliked')
        btn.setAttribute("onclick", 'handle_like(this.id, ' + post_id + ')')
        counter.textContent = updatedCounter
        counter.id = "count_like_" + post_id

      },
      (error) => {
        console.log(error)
      }
    )
}