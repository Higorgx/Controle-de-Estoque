<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { freeSet } from '@coreui/icons'
import { StreamBarcodeReader } from 'vue-barcode-reader'

// Sistema de Toasts
const toasts = ref([])

const showToast = (title, message, color = 'primary', autoHide = true) => {
  const toast = {
    id: Date.now(),
    title,
    message,
    color,
    visible: true
  }
  
  toasts.value.push(toast)
  
  if (autoHide) {
    setTimeout(() => {
      hideToast(toast.id)
    }, 5000)
  }
}

const hideToast = (id) => {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index !== -1) {
    toasts.value[index].visible = false
    setTimeout(() => {
      toasts.value.splice(index, 1)
    }, 300)
  }
}

// Dados simulados de produtos
const fakeProdutos = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  codigo_interno: `PROD${String(i + 1).padStart(3, '0')}`,
  nome: `Produto ${i + 1}`,
  descricao: `Descrição detalhada do produto ${i + 1}`,
  preco: parseFloat((Math.random() * 1000 + 10).toFixed(2)),
  estoque: Math.floor(Math.random() * 100),
  unidade_medida: ['un', 'kg', 'l', 'm'][Math.floor(Math.random() * 4)],
  marca: ['Marca A', 'Marca B', 'Marca C', 'Marca D'][Math.floor(Math.random() * 4)],
  codigo_barras: `789${String(Math.floor(Math.random() * 1000000000)).padStart(9, '0')}`,
  ativo: Math.random() > 0.3,
  fornecedor_id: Math.floor(Math.random() * 3) + 1
}))

// Estado da aplicação
const produtos = ref([])
const produtosParaContagem = ref([])
const loading = ref(true)
const filtro = ref('')
const termoBusca = ref('')
const mostrarApenasDivergentes = ref(false)
const dropdownAberto = ref(false)

const state = ref({
  scannerAtivo: true,
  textoScanner: ''
})
const modalScanner = ref(false)

// Carregar produtos (simulado)
const carregarProdutos = async () => {
  loading.value = true
  try {
    // Simula delay de API
    await new Promise(resolve => setTimeout(resolve, 800))
    produtos.value = fakeProdutos.map(p => ({
      ...p,
      contagemFisica: null,
      diferenca: 0,
      adicionado: false
    }))
  } catch (error) {
    showToast('Erro', 'Erro ao carregar produtos', 'danger')
    console.error('Erro ao carregar produtos:', error)
  } finally {
    loading.value = false
  }
}

const onDecode = (result) => {
  showToast('Sucesso', `Código lido: ${result}`, 'success')
  termoBusca.value = result
  state.value.textoScanner = result
  abrirDropdown()
  // Fecha o modal após 1 segundo
  setTimeout(() => {
    modalScanner.value = false
    state.value.scannerAtivo = true
    state.value.textoScanner =''
  }, 1000)
}

const onLoaded = () => {
  console.log('Scanner carregado')
  state.value.scannerAtivo = true
}

// Produtos disponíveis para adição
const produtosDisponiveis = computed(() => {
  if (!dropdownAberto.value) return []
  
  const produtosNaoAdicionados = produtos.value.filter(p => 
    !produtosParaContagem.value.some(added => added.id === p.id)
  )

  if (!termoBusca.value) {
    return produtosNaoAdicionados.slice(0, 10)
  }

  const termo = termoBusca.value.toLowerCase()
  return produtosNaoAdicionados.filter(p => 
    p.codigo_interno.toLowerCase().includes(termo) ||
    p.nome.toLowerCase().includes(termo) ||
    p.codigo_barras.includes(termo)
  )
})

// Abrir dropdown e garantir dados carregados
const abrirDropdown = () => {
  if (!dropdownAberto.value) {
    dropdownAberto.value = true
    // Adiciona o event listener quando o dropdown abre
    document.addEventListener('click', fecharDropdownAoClicarFora)
  }
  if (produtos.value.length === 0) {
    carregarProdutos()
  }
}
const fecharDropdownAoClicarFora = (event) => {
  const dropdownElement = document.querySelector('.dropdown-menu')
  const inputElement = document.querySelector('input[placeholder="Digite código, nome ou código de barras"]')
  
  // Verifica se o clique foi fora do dropdown e do input
  if (!dropdownElement.contains(event.target) && !inputElement.contains(event.target)) {
    dropdownAberto.value = false
    // Remove o event listener quando o dropdown fecha
    document.removeEventListener('click', fecharDropdownAoClicarFora)
  }
}

// Adicionar produto à contagem
const adicionarProduto = (produto) => {
  if (!produtosParaContagem.value.some(p => p.id === produto.id)) {
    produtosParaContagem.value.push({
      ...produto,
      contagemFisica: null,
      diferenca: 0
    })
    const index = produtos.value.findIndex(p => p.id === produto.id)
    if (index !== -1) {
      produtos.value[index].adicionado = true
    }
    showToast('Sucesso', `${produto.nome} adicionado à contagem`, 'success')
  } else {
    showToast('Aviso', 'Produto já adicionado', 'warning')
  }
  termoBusca.value = ''
  dropdownAberto.value = false
}

// Atualizar contagem física
const atualizarContagem = (produtoId, valor) => {
  const produto = produtosParaContagem.value.find(p => p.id === produtoId)
  if (produto) {
    produto.contagemFisica = valor
    produto.diferenca = (produto.contagemFisica || 0) - produto.estoque
  }
}

// Remover produto da contagem
const removerProduto = (produtoId) => {
  const produto = produtosParaContagem.value.find(p => p.id === produtoId)
  if (produto) {
    produtosParaContagem.value = produtosParaContagem.value.filter(p => p.id !== produtoId)
    const index = produtos.value.findIndex(p => p.id === produtoId)
    if (index !== -1) {
      produtos.value[index].adicionado = false
    }
    showToast('Info', `${produto.nome} removido da contagem`, 'info')
  }
}

// Salvar contagem (simulado)
const salvarContagem = async () => {
  try {
    if (produtosParaContagem.value.length === 0) {
      showToast('Atenção', 'Nenhum produto foi adicionado para contagem!', 'warning')
      return
    }
    
    const produtosContados = produtosParaContagem.value.filter(p => p.contagemFisica !== null)
    
    if (produtosContados.length === 0) {
      showToast('Atenção', 'Nenhum produto foi contado!', 'warning')
      return
    }
    
    // Simula chamada API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showToast('Sucesso', `Contagem de ${produtosContados.length} produtos salva com sucesso!`, 'success')
    
    console.log('Dados para enviar:', produtosContados)
    
  } catch (error) {
    showToast('Erro', 'Erro ao salvar contagem', 'danger')
    console.error('Erro ao salvar contagem:', error)
  }
}

// Filtrar produtos para exibição na tabela
const produtosFiltrados = computed(() => {
  let filtrados = produtosParaContagem.value
  
  if (filtro.value) {
    const termo = filtro.value.toLowerCase()
    filtrados = filtrados.filter(p => 
      p.codigo_interno.toLowerCase().includes(termo) ||
      p.nome.toLowerCase().includes(termo) ||
      p.codigo_barras.includes(termo)
    )
  }
  
  if (mostrarApenasDivergentes.value) {
    filtrados = filtrados.filter(p => p.diferenca !== 0)
  }
  
  return filtrados
})

// Formatar diferença
const formatDiferença = (value) => {
  if (value === 0) return '0'
  return value > 0 ? `+${value}` : value
}

// Formatar preço
const formatPrice = (value) => {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

// Carregar dados iniciais
onMounted(() => {
  carregarProdutos()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', fecharDropdownAoClicarFora)
})

</script>

<template>
  <div class="contagem-estoque-wrapper">
    <CContainer fluid>
      <!-- Card de Busca e Adição -->
      <CCard class="mb-4">
        <CCardHeader>
          <strong>Adicionar Produtos</strong>
        </CCardHeader>
        <CCardBody>
          <CRow class="g-3 align-items-end">
            <CCol :md="8">
              <div class="position-relative">
                <CFormLabel>Buscar Produto</CFormLabel>
                <CInputGroup>
                  <CInputGroupText @click="modalScanner = true" class="cursor-pointer" title="Ler código de barras">
                    <CIcon :name="freeSet.cilBarcode" />
                  </CInputGroupText>
                  <CFormInput
                    v-model="termoBusca"
                    placeholder="Digite código, nome ou código de barras"
                    @focus="abrirDropdown"
                  />
                  
                  <!-- Dropdown de resultados -->
                  <div 
                    v-if="dropdownAberto && produtosDisponiveis.length > 0"
                    class="dropdown-menu show w-100 mt-5"
                    style="position: absolute; z-index: 1000; max-height: 300px; overflow-y: auto;"
                  >
                    <div class="dropdown-header" v-if="!termoBusca">
                      <small>Produtos disponíveis (10 primeiros)</small>
                    </div>
                    <div 
                      v-for="produto in produtosDisponiveis" 
                      :key="produto.id"
                      class="dropdown-item cursor-pointer"
                      @mousedown="adicionarProduto(produto)"
                    >
                      <div class="fw-semibold">{{ produto.nome }}</div>
                      <div class="small text-body-secondary">
                        {{ produto.codigo_interno }} | {{ produto.codigo_barras }} | 
                        Estoque: {{ produto.estoque }} | {{ formatPrice(produto.preco) }}
                      </div>
                    </div>
                    <div class="dropdown-item text-center small text-body-secondary" 
                         v-if="!termoBusca && produtosDisponiveis.length === 10">
                      <em>Digite para buscar mais produtos</em>
                    </div>
                  </div>
                </CInputGroup>
              </div>
            </CCol>
            <CCol :md="4" class="text-end">
              <CButton color="primary" @click="salvarContagem">
                <CIcon :name="freeSet.cilSave" /> Salvar Contagem
              </CButton>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>
      
      <CModal alignment="center" :visible="modalScanner" @close="() => { modalScanner = false; state.scannerAtivo = false }">
        <CModalHeader>
          <CModalTitle>Leitor de Código de Barras</CModalTitle>
        </CModalHeader>
        <CModalBody class="text-center">
          <div v-if="state.scannerAtivo">
            <StreamBarcodeReader
              @decode="onDecode"
              @loaded="onLoaded"
            ></StreamBarcodeReader>
            <p class="mt-3">Aponte para o código de barras</p>
          </div>
          <div v-else>
            <CSpinner />
            <p>Carregando scanner...</p>
          </div>
          
          <div v-if="state.textoScanner" class="mt-3 p-2 bg-light rounded">
            <strong>Código lido:</strong> {{ state.textoScanner }}
          </div>
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" @click="() => { modalScanner = false; state.scannerAtivo = false }">
            Fechar
          </CButton>
        </CModalFooter>
      </CModal>

      <!-- Card de Filtros -->
      <CCard class="mb-4">
        <CCardHeader>
          <strong>Filtros</strong>
        </CCardHeader>
        <CCardBody>
          <CRow class="g-3 align-items-center">
            <CCol :md="6">
              <CFormInput
                v-model="filtro"
                placeholder="Filtrar produtos adicionados..."
              />
            </CCol>
            <CCol :md="6">
              <CFormCheck
                id="mostrarDivergentes"
                v-model="mostrarApenasDivergentes"
                label="Mostrar apenas divergências"
              />
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <!-- Card de Listagem -->
      <CCard>
        <CCardHeader>
          <div class="d-flex justify-content-between align-items-center">
            <strong>Produtos para Contagem</strong>
            <CBadge color="info">
              {{ produtosParaContagem.length }} itens adicionados
            </CBadge>
          </div>
        </CCardHeader>
        <CCardBody>
          <div v-if="loading" class="text-center my-5">
            <CSpinner color="primary" />
            <p>Carregando produtos...</p>
          </div>

          <CTable v-else striped hover responsive>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell width="50px"></CTableHeaderCell>
                <CTableHeaderCell>Código</CTableHeaderCell>
                <CTableHeaderCell>Produto</CTableHeaderCell>
                <CTableHeaderCell>Estoque Sistema</CTableHeaderCell>
                <CTableHeaderCell>Contagem Física</CTableHeaderCell>
                <CTableHeaderCell>Diferença</CTableHeaderCell>
                <CTableHeaderCell width="120px">Ações</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow v-for="produto in produtosFiltrados" :key="produto.id">
                <CTableDataCell>
                  <CBadge :color="produto.ativo ? 'success' : 'secondary'">
                    {{ produto.ativo ? 'Ativo' : 'Inativo' }}
                  </CBadge>
                </CTableDataCell>
                <CTableDataCell>{{ produto.codigo_interno }}</CTableDataCell>
                <CTableDataCell>
                  <div class="fw-semibold">{{ produto.nome }}</div>
                  <div class="small text-body-secondary">
                    {{ produto.marca }} | {{ produto.codigo_barras }}
                  </div>
                </CTableDataCell>
                <CTableDataCell class="text-end">
                  {{ produto.estoque }} {{ produto.unidade_medida }}
                </CTableDataCell>
                <CTableDataCell>
                  <CFormInput
                    type="number"
                    min="0"
                    :value="produto.contagemFisica"
                    @input="atualizarContagem(produto.id, $event.target.valueAsNumber)"
                    class="text-end"
                  />
                </CTableDataCell>
                <CTableDataCell 
                  class="text-end fw-bold"
                  :class="{
                    'text-success': produto.diferenca === 0,
                    'text-danger': produto.diferenca < 0,
                    'text-warning': produto.diferenca > 0
                  }"
                >
                  {{ formatDiferença(produto.diferenca) }}
                </CTableDataCell>
                <CTableDataCell>
                  <div class="d-flex gap-2">
                    <CButton 
                      color="secondary" 
                      size="sm"
                      @click="atualizarContagem(produto.id, produto.estoque)"
                      title="Usar valor do sistema"
                    >
                      <CIcon :name="freeSet.cilReload" />
                    </CButton>
                    <CButton 
                      color="danger" 
                      size="sm"
                      @click="removerProduto(produto.id)"
                      title="Remover"
                    >
                      <CIcon :name="freeSet.cilTrash" />
                    </CButton>
                  </div>
                </CTableDataCell>
              </CTableRow>
              <CTableRow v-if="produtosFiltrados.length === 0">
                <CTableDataCell colspan="7" class="text-center">
                  <template v-if="produtosParaContagem.length === 0">
                    Nenhum produto adicionado à contagem
                  </template>
                  <template v-else>
                    Nenhum produto corresponde aos filtros aplicados
                  </template>
                </CTableDataCell>
              </CTableRow>
            </CTableBody>
          </CTable>
        </CCardBody>
      </CCard>

      <!-- Resumo da Contagem -->
      <CCard class="mt-4">
        <CCardHeader>
          <strong>Resumo da Contagem</strong>
        </CCardHeader>
        <CCardBody>
          <CRow>
            <CCol :md="4">
              <div class="border-start border-start-4 border-start-primary py-1 px-3 mb-3">
                <div class="text-body-secondary small">Total de Itens</div>
                <div class="fs-5 fw-semibold">{{ produtosParaContagem.length }}</div>
              </div>
            </CCol>
            <CCol :md="4">
              <div class="border-start border-start-4 border-start-success py-1 px-3 mb-3">
                <div class="text-body-secondary small">Itens Contados</div>
                <div class="fs-5 fw-semibold">
                  {{ produtosParaContagem.filter(p => p.contagemFisica !== null).length }}
                </div>
              </div>
            </CCol>
            <CCol :md="4">
              <div class="border-start border-start-4 border-start-warning py-1 px-3 mb-3">
                <div class="text-body-secondary small">Divergências</div>
                <div class="fs-5 fw-semibold">
                  {{ produtosParaContagem.filter(p => p.diferenca !== 0).length }}
                </div>
              </div>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <!-- Toaster container -->
      <CToaster placement="top-end">
        <CToast 
          v-for="toast in toasts" 
          :key="toast.id"
          :color="toast.color"
          :visible="toast.visible"
          :autohide="false"
        >
          <CToastHeader closeButton @close="hideToast(toast.id)">
            <span class="me-auto fw-bold">{{ toast.title }}</span>
            <small>Agora</small>
          </CToastHeader>
          <CToastBody>
            {{ toast.message }}
          </CToastBody>
        </CToast>
      </CToaster>
    </CContainer>
  </div>
</template>

<style scoped>
.contagem-estoque-wrapper {
  padding: 1rem 0;
}

.card {
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.dropdown-item {
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.dropdown-item:hover {
  background-color: #f8f9fa;
}
.dropdown-header {
  padding: 0.25rem 1rem;
  font-size: 0.875rem;
  color: #6c757d;
  background-color: #f8f9fa;
}
.cursor-pointer {
  cursor: pointer;
}

.text-success {
  color: #2eb85c !important;
}
.text-danger {
  color: #e55353 !important;
}
.text-warning {
  color: #f9b115 !important;
}

input[type='number'] {
  text-align: right;
  max-width: 120px;
  margin: 0 auto;
  display: block;
}

.table-responsive {
  overflow-x: auto;
}

@media (max-width: 768px) {
  .d-flex.gap-2 {
    gap: 0.5rem !important;
  }
  .btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
  }
}
</style>