const countryDB = {
  _prevCity: '',
  _previousNationality: '',
  setCity: (prevCity, previousNationality) => {
    if (
      prevCity !== countryDB._prevCity &&
      prevCity !== '' &&
      previousNationality !== countryDB._previousNationality
    ) {
      countryDB._prevCity = prevCity
      countryDB._previousNationality = previousNationality
    }
  },
}

document.addEventListener('DOMContentLoaded', function () {
  var nationality = document.querySelector('.user_address_country')
  var city = document.querySelector('.user_address_city')
  countryDB.setCity(city.value, nationality.value)

  // Replace with the actual dependent field ID
  function appendSelectChild(text, value) {
    var option = document.createElement('option')
    option.text = text
    option.value = value
    return option
  }

  // Function to update the dependent field options based on the selected category
  function updateDependentFieldOptions() {
    var selectedNationality = nationality.value

    if (selectedNationality) {
      fetch('/auth/user/cities/?country_code=' + selectedNationality)
        .then(function (response) {
          if (response.ok) {
            return response.json()
          } else {
            throw new Error('Error retrieving dependent options')
          }
        })
        .then(function (data) {
          city.innerHTML = ''
          for (var key in data) {
            if (data.hasOwnProperty(key)) {
              city.appendChild(appendSelectChild(data[key], key))
            }
          }
          city.disabled = false
          if (countryDB._previousNationality === selectedNationality)
            city.value = countryDB._prevCity
          else {
            city.value = ''
          }
        })
        .catch(function (error) {
          if (!city.value) {
            city.innerHTML = ''
            city.appendChild(
              appendSelectChild('---------select a nationality---------', ''),
            )
            city.disabled = true
          }
          selectedNationality == ''
            ? (nationality.value = '')
            : (nationality.value = selectedNationality)
        })
    } else {
      city.innerHTML = ''
      city.appendChild(
        appendSelectChild('---------select a nationality---------', ''),
      )
      city.disabled = true
    }
  }
  if (nationality) {
    // Attach an event listener to the category field
    nationality.addEventListener('change', updateDependentFieldOptions)

    // Update the dependent field options on page load
    updateDependentFieldOptions()
  }
})
