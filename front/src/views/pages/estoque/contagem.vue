<script setup>
import { ref, onMounted, computed, onBeforeUnmount, watch } from 'vue'
import { freeSet } from '@coreui/icons'
import { StreamBarcodeReader } from 'vue-barcode-reader'
import { getCurrentInstance } from 'vue'
import { debounce } from 'lodash'

// Acessa a instância do Axios injetada globalmente
const { proxy } = getCurrentInstance()
const api = proxy.$api

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

// Estado da aplicação
const produtos = ref([])
const produtosParaContagem = ref([])
const loading = ref(false)
const filtro = ref('')
const termoBusca = ref('')
const mostrarApenasDivergentes = ref(false)
const dropdownAberto = ref(false)
const buscandoProdutos = ref(false)

const state = ref({
  scannerAtivo: true,
  textoScanner: ''
})
const modalScanner = ref(false)

// Busca produtos na API com debounce
const buscarProdutosAPI = debounce(async (termo) => {
  if (!termo || termo.length < 2) {
    produtos.value = []
    dropdownAberto.value = false
    return
  }

  buscandoProdutos.value = true
  dropdownAberto.value = true
  
  try {
    const response = await api.get('/produto/filtro', {
      params: {
        busca_geral: termo,
        limit: 10
      }
    })
    
    produtos.value = response.data.map(p => ({
      ...p,
      contagemFisica: null,
      diferenca: 0,
      adicionado: false
    }))
  } catch (error) {
    showToast('Erro', 'Falha ao buscar produtos', 'danger')
    console.error('Erro ao buscar produtos:', error)
  } finally {
    buscandoProdutos.value = false
  }
}, 300)

// Watch para o termo de busca
watch(termoBusca, (novoTermo) => {
  buscarProdutosAPI(novoTermo)
})

const onDecode = async (result) => {
  showToast('Sucesso', `Código lido: ${result}`, 'success')
  state.value.textoScanner = result
  
  try {
    modalScanner.value = false
    state.value.scannerAtivo = true
    
    // Busca exata pelo código de barras
    const response = await api.get('/produto/filtro', {
      params: { codigo_barras: result }
    })
    
    if (response.data.length > 0) {
      adicionarProduto(response.data[0])
    } else {
      termoBusca.value = result
      abrirDropdown()
      showToast('Aviso', 'Produto não encontrado. Verifique o código.', 'warning')
    }
  } catch (error) {
    console.error('Erro ao buscar produto:', error)
    termoBusca.value = result
    abrirDropdown()
  }
}

const onLoaded = () => {
  state.value.scannerAtivo = true
}

// Produtos disponíveis para adição
const produtosDisponiveis = computed(() => {
  if (!dropdownAberto.value) return []
  return produtos.value.filter(p => 
    !produtosParaContagem.value.some(added => added.id === p.id)
  )
})

const abrirDropdown = () => {
  if (!dropdownAberto.value) {
    dropdownAberto.value = true
    document.addEventListener('click', fecharDropdownAoClicarFora)
  }
}

const fecharDropdownAoClicarFora = (event) => {
  const dropdownElement = document.querySelector('.dropdown-menu')
  const inputElement = document.querySelector('input[placeholder="Digite código, nome ou código de barras"]')
  
  if (!dropdownElement?.contains(event.target) && !inputElement?.contains(event.target)) {
    dropdownAberto.value = false
    document.removeEventListener('click', fecharDropdownAoClicarFora)
  }
}

const adicionarProduto = (produto) => {
  if (!produtosParaContagem.value.some(p => p.id === produto.id)) {
    produtosParaContagem.value.push({
      ...produto,
      contagemFisica: null,
      diferenca: 0
    })
    showToast('Sucesso', `${produto.nome} adicionado à contagem`, 'success')
  } else {
    showToast('Aviso', 'Produto já adicionado', 'warning')
  }
  termoBusca.value = ''
  dropdownAberto.value = false
}

const atualizarContagem = (produtoId, valor) => {
  const produto = produtosParaContagem.value.find(p => p.id === produtoId)
  if (produto) {
    produto.contagemFisica = valor
    produto.diferenca = (produto.contagemFisica || 0) - produto.estoque
  }
}

const removerProduto = (produtoId) => {
  const produto = produtosParaContagem.value.find(p => p.id === produtoId)
  if (produto) {
    produtosParaContagem.value = produtosParaContagem.value.filter(p => p.id !== produtoId)
    showToast('Info', `${produto.nome} removido da contagem`, 'info')
  }
}

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
    
    await api.post('/contagem-estoque', {
      produtos: produtosContados.map(p => ({
        produto_id: p.id,
        estoque_sistema: p.estoque,
        contagem_fisica: p.contagemFisica,
        diferenca: p.diferenca
      })),
      data: new Date().toISOString()
    })
    
    showToast('Sucesso', `Contagem salva (${produtosContados.length} itens)`, 'success')
    
  } catch (error) {
    const errorMessage = error.response?.data?.message || 'Erro ao salvar contagem'
    showToast('Erro', errorMessage, 'danger')
    console.error('Erro ao salvar contagem:', error)
  }
}

const produtosFiltrados = computed(() => {
  let filtrados = produtosParaContagem.value
  
  if (filtro.value) {
    const termo = filtro.value.toLowerCase()
    filtrados = filtrados.filter(p => 
      p.codigo_interno.toLowerCase().includes(termo) ||
      p.nome.toLowerCase().includes(termo) ||
      p.codigo_barras?.includes(termo)
    )
  }
  
  if (mostrarApenasDivergentes.value) {
    filtrados = filtrados.filter(p => p.diferenca !== 0)
  }
  
  return filtrados
})

const formatDiferença = (value) => {
  if (value === 0) return '0'
  return value > 0 ? `+${value}` : value
}

const formatPrice = (value) => {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

onMounted(() => {
  document.addEventListener('click', fecharDropdownAoClicarFora)
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
                    v-if="dropdownAberto"
                    class="dropdown-menu show w-100 mt-5"
                    style="position: absolute; z-index: 1000; max-height: 300px; overflow-y: auto;"
                  >
                    <div v-if="buscandoProdutos" class="text-center p-2">
                      <CSpinner size="sm" /> Buscando produtos...
                    </div>
                    
                    <div 
                      v-else-if="produtosDisponiveis.length > 0"
                      v-for="produto in produtosDisponiveis" 
                      :key="produto.id"
                      class="dropdown-item cursor-pointer"
                      @click="adicionarProduto(produto)"
                    >
                      <div class="fw-semibold">{{ produto.nome }}</div>
                      <div class="small text-body-secondary">
                        {{ produto.codigo_interno }} | {{ produto.codigo_barras || 'Sem código' }} | 
                        Estoque: {{ produto.estoque }} | {{ formatPrice(produto.preco) }}
                      </div>
                    </div>
                    
                    <div v-else-if="termoBusca.length >= 2" class="dropdown-item text-center small text-body-secondary">
                      <em>Nenhum produto encontrado</em>
                    </div>
                    
                    <div v-else class="dropdown-item text-center small text-body-secondary">
                      <em>Digite pelo menos 2 caracteres</em>
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
      
      <!-- Modal do Scanner -->
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
          <CTable striped hover responsive>
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
                    {{ produto.marca }} | {{ produto.codigo_barras || 'Sem código' }}
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

