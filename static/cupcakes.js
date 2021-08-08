const BASE_URL = 'http://localhost:5000/api';

function createCupcakeHTML(cupcake) {
  cupcakeHTML = `<div data-cupcake-id=${cupcake.id}>
        <li>
            ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
            <button class="delete-cupcake"><i class="lni lni-trash-can"></i></button>
        </li>
        <img class="cupcake-image" src="${cupcake.image}" alt="${cupcake.flavor} image"
    </div>
        `;
  return cupcakeHTML;
}

async function displayCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(createCupcakeHTML(cupcakeData));
    $('#cupcake-list').append(newCupcake);
  }
}

$('#cupcake-form').on('submit', async function (evt) {
  evt.preventDefault();

  console.log('clicked');

  let flavor = $('#flavor').val();
  let rating = $('#rating').val();
  let size = $('#size').val();
  let image = $('#image').val();

  const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });

  let newCupcake = $(createCupcakeHTML(newCupcakeResp.data.cupcake));
  console.log(newCupcakeResp.data.cupcake.image);
  $('#cupcake-list').append(newCupcake);
  $('#cupcake-form').trigger('reset');
});

$('#cupcake-list').on('click', '.delete-cupcake', async function (evt) {
  evt.preventDefault();

  let $cupcake = $(evt.target).closest('div');
  let cupcakeId = $cupcake.attr('data-cupcake-id');

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

$(displayCupcakes);
