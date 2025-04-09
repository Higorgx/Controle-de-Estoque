<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Fake backend - dados simulados
const fakeProdutos = Array.from({ length: 45 }, (_, i) => ({
  id: i + 1,
  codigo_interno: `PROD${String(i + 1).padStart(3, '0')}`,
  nome: `Produto ${i + 1}`,
  descricao: `Descrição do produto ${i + 1}`,
  preco: parseFloat((Math.random() * 100 + 5).toFixed(2)),
  estoque: Math.floor(Math.random() * 100),
  unidade_medida: ['un', 'kg', 'l', 'm'][Math.floor(Math.random() * 4)],
  marca: ['Marca A', 'Marca B', 'Marca C', 'Marca D'][Math.floor(Math.random() * 4)],
  codigo_barras: `789${String(Math.floor(Math.random() * 1000000000)).padStart(9, '0')}`,
  ativo: Math.random() > 0.3,
  fornecedor_id: Math.floor(Math.random() * 3) + 1,
  fornecedor: {
    id: Math.floor(Math.random() * 3) + 1,
    nome: ['Fornecedor X', 'Fornecedor Y', 'Fornecedor Z'][Math.floor(Math.random() * 3)]
  }
}))

const fakeFornecedores = [
  { id: 1, nome: 'Fornecedor X' },
  { id: 2, nome: 'Fornecedor Y' },
  { id: 3, nome: 'Fornecedor Z' }
]

// Simular chamada API com delay
const fakeApiCall = (data, delay = 500) => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve({ data })
    }, delay)
  })
}

// Estado dos produtos e paginação
const produtos = ref([])
const loading = ref(true)
const error = ref(null)
const totalItems = ref(0)
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalPages = ref(1)

// Filtros
let filters_request = ref({
  nome: '',
  codigo_interno: '',
  codigo_barras: '',
  ativo: 'todos',
  fornecedor_id: null
})

const filters = ref({
  nome: '',
  codigo_interno: '',
  codigo_barras: '',
  ativo: 'todos',
  fornecedor_id: null
})



// Buscar produtos (fake)
const fetchProdutos = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Simular delay da API
    await fakeApiCall(null, 300)
    
    // Aplicar filtros
    let filtered = [...fakeProdutos]

    filters_request = filters
    
    if (filters_request.value.nome) {
      filtered = filtered.filter(p => 
        p.nome.toLowerCase().includes(filters_request.value.nome.toLowerCase())
      )
    }
    
    if (filters_request.value.codigo_interno) {
      filtered = filtered.filter(p => 
        p.codigo_interno.includes(filters_request.value.codigo_interno)
      )
    }
    
    if (filters_request.value.codigo_barras) {
      filtered = filtered.filter(p => 
        p.codigo_barras.includes(filters_request.value.codigo_barras)
      )
    }
    
    if (filters_request.value.ativo !== 'todos') {
      const status = filters_request.value.ativo === 'ativo'
      filtered = filtered.filter(p => p.ativo === status)
    }
    
    if (filters_request.value.fornecedor_id) {
      filtered = filtered.filter(p => 
        p.fornecedor_id === filters_request.value.fornecedor_id
      )
    }
    
    // Paginação
    totalItems.value = filtered.length
    totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value)
    
    const start = (currentPage.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    produtos.value = filtered.slice(start, end)
    
  } catch (err) {
    error.value = 'Erro ao carregar produtos'
    console.error('Erro:', err)
  } finally {
    loading.value = false
  }
}

// Buscar fornecedores (fake)
const fetchFornecedores = async () => {
  try {
    await fakeApiCall(null, 200)
    fornecedores.value = fakeFornecedores
  } catch (err) {
    console.error('Erro ao buscar fornecedores:', err)
  }
}

// Editar produto
const editProduto = (id) => {
  router.push(`/produtos/editar/${id}`)
}

// Inativar/Ativar produto (fake)
const toggleStatus = async (produto) => {
  if (!confirm(`Tem certeza que deseja ${produto.ativo ? 'inativar' : 'ativar'} este produto?`)) {
    return
  }

  try {
    // Simular chamada API
    await fakeApiCall(null, 200)
    
    // Atualizar localmente
    const index = fakeProdutos.findIndex(p => p.id === produto.id)
    if (index !== -1) {
      fakeProdutos[index].ativo = !fakeProdutos[index].ativo
      fetchProdutos()
    }
  } catch (err) {
    alert('Erro ao alterar status do produto')
    console.error('Erro:', err)
  }
}

// Resetar filtros
const resetFilters = () => {
  filters.value = {
    nome: '',
    codigo_interno: '',
    codigo_barras: '',
    ativo: 'todos',
    fornecedor_id: null
  }
  currentPage.value = 1
}

// Formatar preço
const formatPrice = (value) => {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}

// Formatar status
const formatStatus = (ativo) => {
  return ativo ? 'Ativo' : 'Inativo'
}

// Observar mudanças
watch([currentPage, itemsPerPage], fetchProdutos)

watch(
  () => {
    currentPage.value = 1
    fetchProdutos()
  },
  { deep: true }
)

// Carregar dados iniciais
onMounted(() => {
  fetchProdutos()
  fetchFornecedores()
})
</script>

<template>
  <div class="product-list-wrapper">
    <CContainer fluid>
            <!-- Card de Filtros -->
      <CCard class="mb-4">
        <CCardHeader>
          <strong>Filtros</strong>
        </CCardHeader>
        <CCardBody>
          <CRow class="g-3">
            <CCol :md="4">
              <CFormLabel for="filterNome">Nome</CFormLabel>
              <CFormInput
                id="filterNome"
                v-model="filters.nome"
                placeholder="Filtrar por nome"
              />
            </CCol>

            <CCol :md="2">
              <CFormLabel for="filterCodigoInterno">Código Interno</CFormLabel>
              <CFormInput
                id="filterCodigoInterno"
                v-model="filters.codigo_interno"
                placeholder="Código interno"
              />
            </CCol>

            <CCol :md="2">
              <CFormLabel for="filterCodigoBarras">Código de Barras</CFormLabel>
              <CFormInput
                id="filterCodigoBarras"
                v-model="filters.codigo_barras"
                placeholder="Código de barras"
              />
            </CCol>

            <CCol :md="2">
              <CFormLabel for="filterStatus">Status</CFormLabel>
              <CFormSelect id="filterStatus" v-model="filters.ativo">
                <option value="todos">Todos</option>
                <option value="ativo">Ativos</option>
                <option value="inativo">Inativos</option>
              </CFormSelect>
            </CCol>

            <CCol :md="2">
              <CFormLabel for="filterFornecedor">Fornecedor</CFormLabel>
              <CFormSelect id="filterFornecedor" v-model="filters.fornecedor_id">
                <option :value="null">Todos</option>
                <option 
                  v-for="fornecedor in fornecedores" 
                  :key="fornecedor.id" 
                  :value="fornecedor.id"
                >
                  {{ fornecedor.nome }}
                </option>
              </CFormSelect>
            </CCol>

            <CCol :xs="12" class="mt-2">
              <div class="d-flex justify-content-end gap-2">
                <CButton color="secondary" @click="resetFilters">
                  Limpar Filtros
                </CButton>
                <CButton color="primary" @click="fetchProdutos">
                  Aplicar Filtros
                </CButton>
              </div>
            </CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <!-- Card de Listagem -->
      <CCard>
        <CCardHeader>
          <div class="d-flex justify-content-between align-items-center">
            <strong>Produtos Cadastrados</strong>
            <CButton color="success" @click="router.push('/produto/cadastro')">
              <CIcon name="cil-plus" />Novo Produto
            </CButton>
          </div>
        </CCardHeader>
        <CCardBody>
          <CAlert v-if="error" color="danger">{{ error }}</CAlert>

          <div v-if="loading" class="text-center my-5">
            <CSpinner color="primary" />
            <p>Carregando produtos...</p>
          </div>

          <CTable v-if="!loading" striped hover responsive>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell>Código interno</CTableHeaderCell>
                <CTableHeaderCell>Nome</CTableHeaderCell>
                <CTableHeaderCell>Preço</CTableHeaderCell>
                <CTableHeaderCell>Estoque</CTableHeaderCell>
                <CTableHeaderCell>Fornecedor</CTableHeaderCell>
                <CTableHeaderCell>Status</CTableHeaderCell>
                <CTableHeaderCell width="120px">Ações</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow v-for="produto in produtos" :key="produto.id">
                <CTableDataCell>{{ produto.codigo_interno }}</CTableDataCell>
                <CTableDataCell>{{ produto.nome }}</CTableDataCell>
                <CTableDataCell>{{ formatPrice(produto.preco) }}</CTableDataCell>
                <CTableDataCell>{{ produto.estoque }} {{ produto.unidade_medida }}</CTableDataCell>
                <CTableDataCell>{{ produto.fornecedor?.nome || '-' }}</CTableDataCell>
                <CTableDataCell>
                  <CBadge :color="produto.ativo ? 'success' : 'secondary'">
                    {{ formatStatus(produto.ativo) }}
                  </CBadge>
                </CTableDataCell>
                <CTableDataCell>
                  <div class="d-flex gap-2">
                    <CButton 
                      color="primary" 
                      size="sm"
                      @click="editProduto(produto.id)"
                      title="Editar"
                    >
                      <CIcon name="cil-pencil" />
                    </CButton>
                    <CButton 
                      :color="produto.ativo ? 'danger' : 'success'" 
                      size="sm"
                      @click="toggleStatus(produto)"
                      :title="produto.ativo ? 'Inativar' : 'Ativar'"
                    >
                      <CIcon :name="produto.ativo ? 'cil-ban' : 'cil-check'" />
                    </CButton>
                  </div>
                </CTableDataCell>
              </CTableRow>
              <CTableRow v-if="produtos.length === 0">
                <CTableDataCell colspan="7" class="text-center">
                  Nenhum produto encontrado
                </CTableDataCell>
              </CTableRow>
            </CTableBody>
          </CTable>

          <!-- Paginação -->
          <div v-if="!loading && produtos.length > 0" class="d-flex justify-content-between mt-3">
            <div class="d-flex align-items-center">
              <span class="me-2">Itens por página:</span>
              <CFormSelect v-model="itemsPerPage" style="width: 80px" class="me-3">
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
              </CFormSelect>
              <span>
                Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }} a 
                {{ Math.min(currentPage * itemsPerPage, totalItems) }} de 
                {{ totalItems }} itens
              </span>
            </div>
            <CPagination v-model="currentPage" :pages="totalPages" align="end" />
          </div>
        </CCardBody>
      </CCard>
    </CContainer>
  </div>
</template>
