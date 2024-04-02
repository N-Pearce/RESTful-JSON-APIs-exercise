const BASE_URL = 'http://127.0.0.1:5000/api'
const $cupcakeList = $("#cupcake-list")
const $newCupcakeForm = $('#new-cupk-form')

function generateCupcakeHTML(cupcake){
    return `
        <li cupcake-id=${cupcake.id}>
            Flavor: ${cupcake.flavor} / 
            Rating: ${cupcake.rating} / 
            Size: ${cupcake.size} <br>
            <image class=cupcake-image src=${cupcake.image}><image><br>
            <button class='remove'>Remove</button>
        </li>`
}

async function showCupcakes(){
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $cupcakeList.append(newCupcake);
    }
}

$('#add-cupcake-btn').on('click', async function(e){
    e.preventDefault();

    flavor = $('#cupk-flavor').val()
    rating = $('#cupk-rating').val()
    size = $('#cupk-size').val()
    image = $('#cupk-image').val()

    if (flavor=='' || rating=='' || size=='')
        return;
    
    const resp = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, rating, size, image
    });

    let newCupcake = $(generateCupcakeHTML(resp.data.cupcake))
    $cupcakeList.append(newCupcake)

    $newCupcakeForm.trigger('reset')
});

$cupcakeList.on('click', '.remove', async function(e){
    let $cupcake = $(e.target).closest('li')
    let cupcakeId = $cupcake.attr('cupcake-id')
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)

    $cupcake.remove()
});

$(showCupcakes());