
(async function precargarProductos() {
  try {
    const categorias = await fetch('https://tienda.mercadona.es/api/categories/')
      .then(res => res.json());

    for (const categoria of categorias) {
      const detalle = await fetch(`https://tienda.mercadona.es/api/categories/${categoria.id}/`)
        .then(res => res.json());

      detalle.products.forEach(producto => {
        const dataMinima = {
          id: producto.id,
          nombre: producto.display_name,
          precio: producto.price_instructions.price,
          precio_anterior: producto.price_instructions.reference_price,
          imagen: producto.thumbnail
        };

        localStorage.setItem(`producto_${producto.id}`, JSON.stringify(dataMinima));
      });

      // Puedes añadir un pequeño retardo entre categorías si quieres evitar sobrecargar la red
      await new Promise(res => setTimeout(res, 250));
    }

    console.log('Precarga completa de productos esenciales en localStorage');
  } catch (err) {
    console.error("Error al precargar productos:", err);
  }
})();

