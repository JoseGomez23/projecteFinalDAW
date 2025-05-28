
fetch("static/products.json")
  .then(res => res.json())
  .then(productos => {
    productos.forEach(p => {
      localStorage.setItem(`producto_${p.id}`, JSON.stringify(p));
    });
    console.log("Productos cargados en localStorage sin CORS");
  });

