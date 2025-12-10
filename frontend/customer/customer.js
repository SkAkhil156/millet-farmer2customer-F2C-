// ------- Data -------
const products = [
  {id:1,name:'White Rice',price:90,unit:'kg',img:'images/White Rice.jpg',tags:['Refined grain'],desc:'White rice — polished long-grain rice commonly used in everyday meals.',farmer:'Farmer: Veeresh',phone:'+91-9001122334',rating:4.2,provider:'Veeresh Rice Mills'},
  {id:2,name:'Pearl Millet (Bajra)',price:60,unit:'kg',img:'images/Pearl Millet.webp',tags:['Gluten-free','High fiber'],desc:'Pearl millet — rich in protein and minerals.',farmer:'Farmer: Ramesh & Sons',phone:'+91-9876543210',rating:4.5,provider:'Ramesh Farms'},
  {id:3,name:'Finger Millet (Ragi)',price:80,unit:'kg',img:'images/Finger Millet.jpg',tags:['Calcium rich'],desc:'Excellent source of calcium and iron.',farmer:'Farmer: Lakshmi',phone:'+91-9876512340',rating:4.7,provider:'Lakshmi Agro'},
  {id:4,name:'Sorghum (Jowar)',price:55,unit:'kg',img:'images/Sorghum.webp',tags:['Low GI'],desc:'Sorghum — staple grain for flatbreads.',farmer:'Farmer: Kumar',phone:'+91-9765432109',rating:4.3,provider:'Kumar Farms'},
  {id:5,name:'Foxtail Millet',price:95,unit:'kg',img:'images/Foxtail Millet.jpg',tags:['Micronutrients'],desc:'Cooks quickly and is high in protein.',farmer:'Farmer: Anjali',phone:'+91-9123456780',rating:4.4,provider:'Anjali Organic'},
  {id:6,name:'Little Millet',price:70,unit:'kg',img:'images/Little Millet.webp',tags:['Low fat'],desc:'Easy to digest.',farmer:'Farmer: Suresh',phone:'+91-9988776655',rating:4.1,provider:'Suresh Agro'},
  {id:7,name:'Kodo Millet',price:85,unit:'kg',img:'images/Kodo Millet.jpg',tags:['Antioxidants'],desc:'High in fibre.',farmer:'Farmer: Priya',phone:'+91-9012345678',rating:4.2,provider:'Priya Farms'},
  {id:8,name:'Barnyard Millet',price:75,unit:'kg',img:'images/Barnyard Millet.jpg',tags:['Quick cook'],desc:'Fast cooking grain.',farmer:'Farmer: Raju',phone:'+91-9898989898',rating:4.0,provider:'Raju Farms'},
  {id:9,name:'Proso Millet',price:68,unit:'kg',img:'images/Proso Millet.jpg',tags:['Heart friendly'],desc:'Neutral flavour.',farmer:'Farmer: Geeta',phone:'+91-9776655443',rating:4.0,provider:'Geeta Organics'},
  {id:10,name:'Brown Rice',price:120,unit:'kg',img:'images/Brown Rice.jpg',tags:['Whole grain'],desc:'High fibre.',farmer:'Farmer: Hari',phone:'+91-9665544332',rating:4.6,provider:'Hari Rice Mills'},
  {id:11,name:'Red Rice',price:140,unit:'kg',img:'images/Red Rice.jpg',tags:['Nutty flavor'],desc:'Rich in antioxidants.',farmer:'Farmer: Meera',phone:'+91-9554433221',rating:4.6,provider:'Meera Farms'}
];

let cart = [];

// Helper
function formatRupee(v){ return '₹'+Number(v).toLocaleString('en-IN'); }

// Render product grid
const grid = document.getElementById("productsGrid");
function renderGrid(list){
  grid.innerHTML = "";
  list.forEach(p=>{
    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = `
  <div class="thumb" style="background-image:url('${p.img}')"></div>
  <div class="meta">
    <div>
      <div class="title">${p.name}</div>
      <div class="muted">Provided by ${p.provider}</div>
    </div>
    <div class="price">${formatRupee(p.price)}/${p.unit}</div>
  </div>
  <div style="margin-top:8px;display:flex;justify-content:space-between">
    <div class="tag">${p.tags[0]}</div>
    <div class="stars">${renderStars(p.rating)}</div>
  </div>
  <div class="actions">
    <button class="link-like" onclick="event.stopPropagation(); openDetail(${p.id})">View</button>
    <button class="btn" onclick="event.stopPropagation(); addToCartById(${p.id})">Add</button>
  </div>
`;

    el.onclick = ()=>openDetail(p.id);
    grid.appendChild(el);
  });
  document.getElementById("resultCount").textContent = list.length;
}

function renderStars(r){
  const full = Math.floor(r);
  const half = r-full >= 0.5;
  let out = "";
  for(let i=0;i<full;i++) out += '<span class="star on">★</span>';
  if(half) out += '<span class="star on">☆</span>';
  while(out.replace(/<[^>]+>/g,'').length < 5)
    out += '<span class="star">★</span>';
  return out;
}

// ===== DETAIL MODAL =====
const overlay = document.getElementById("overlay");
const modalTitle = document.getElementById("modalTitle");
const modalImage = document.getElementById("modalImage");
const modalDesc = document.getElementById("modalDesc");
const modalFarmer = document.getElementById("modalFarmer");
const modalPrice = document.getElementById("modalPrice");
const modalRating = document.getElementById("modalRating");
const farmerContact = document.getElementById("farmerContact");
let currentProduct = null;

function openDetail(id){
  const p = products.find(x=>x.id===id);
  currentProduct = p;

  modalTitle.textContent = p.name;
  modalImage.style.backgroundImage = `url('${p.img}')`;
  modalDesc.textContent = p.desc;
  modalFarmer.textContent = p.farmer + " — " + p.provider;
  modalPrice.textContent = formatRupee(p.price) + "/" + p.unit;
  modalRating.innerHTML = renderStars(p.rating);
  farmerContact.textContent = p.phone;

  overlay.style.display = "flex";
}

document.getElementById("closeModal").onclick = ()=> overlay.style.display="none";

overlay.addEventListener("click", e=>{
  if(e.target===overlay) overlay.style.display="none";
});

// Cart functions
function addToCartById(id){
  const p = products.find(x=>x.id===id);
  const found = cart.find(c=>c.id===id);

  if(found) found.qty++;
  else cart.push({...p, qty:1});

  updateCartUI();
}

document.getElementById("addToCartBtn").onclick = ()=>{
  if(currentProduct) addToCartById(currentProduct.id);
  overlay.style.display="none";
};

function updateCartUI(){
  const count = cart.reduce((s,i)=>s+i.qty,0);
  document.getElementById("cartCount").textContent = count;

  const list = document.getElementById("cartList");
  list.innerHTML = "";

  let total = 0;
  cart.forEach(item=>{
    total += item.price * item.qty;
    const div = document.createElement("div");
    div.className = "cart-item";
    div.innerHTML = `
      <div style="flex:1">
        <strong>${item.name}</strong>
        <div class='muted'>${item.provider} · ${formatRupee(item.price)}/${item.unit}</div>
      </div>
      <div style="text-align:right">
        <div style="font-weight:800">${formatRupee(item.price * item.qty)}</div>
        <div style="margin-top:6px">
          <button class='ghost' onclick='decrease(${item.id})'>-</button>
          <span style='padding:6px 10px'>${item.qty}</span>
          <button class='btn' onclick='increase(${item.id})'>+</button>
        </div>
      </div>
    `;
    list.appendChild(div);
  });

  document.getElementById("cartTotal").textContent = formatRupee(total);
  document.getElementById("cartPanel").style.display = cart.length ? "block" : "none";
}

function increase(id){
  const it = cart.find(c=>c.id===id);
  if(it){ it.qty++; updateCartUI(); }
}

function decrease(id){
  const it = cart.find(c=>c.id===id);
  if(it){
    it.qty--;
    if(it.qty<=0) cart = cart.filter(c=>c.id!==id);
    updateCartUI();
  }
}

// Cart panel toggle
document.getElementById("openCart").onclick = ()=>{
  const panel = document.getElementById("cartPanel");
  panel.style.display = panel.style.display==="none" ? "block" : "none";
};

document.getElementById("clearCart").onclick = ()=>{
  cart=[];
  updateCartUI();
};

document.getElementById("checkout").onclick = ()=>{
  if(!cart.length){ alert("Your cart is empty!"); return; }
  alert("Thank you! Total: "+document.getElementById("cartTotal").textContent);
  cart=[];
  updateCartUI();
};

// Search
document.getElementById("searchInput").addEventListener("input", e=>{
  const q = e.target.value.trim().toLowerCase();
  const filtered = products.filter(p =>
    (p.name + p.tags.join(" ") + p.provider + p.farmer).toLowerCase().includes(q)
  );
  renderGrid(filtered);
});

// Buy Now
document.getElementById("buyNowBtn").onclick = ()=>{
  if(currentProduct){
    alert("Buying: "+currentProduct.name);
    overlay.style.display="none";
  }
};

// Initial render
renderGrid(products);
updateCartUI();

// Escape key actions
window.addEventListener("keydown", e=>{
  if(e.key==="Escape"){
    overlay.style.display="none";
    document.getElementById("cartPanel").style.display="none";
  }
});
