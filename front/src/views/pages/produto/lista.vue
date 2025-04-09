<script setup>
import { ref, onMounted, watch, inject } from 'vue'
import { useRouter } from 'vue-router'

const api = inject('api')
const router = useRouter()

// Estado dos produtos e paginação
const produtos = ref([])
const fornecedores = ref([])
const loading = ref(true)
const error = ref(null)
const totalItems = ref(0)
const currentPage = ref(1)
const itemsPerPage = ref(10)
const totalPages = ref(1)

// Filtros
const filters = ref({
  nome: '',
  codigo_interno: '',
  codigo_barras: '',
  ativo: 'todos',
  fornecedor_id: null
})



// Buscar produtos da API
const fetchProdutos = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Construir parâmetros da URL
    const params = new URLSearchParams()
    
    if (filters.value.nome) params.append('nome', filters.value.nome)
    if (filters.value.codigo_interno) params.append('codigo_interno', filters.value.codigo_interno)
    if (filters.value.codigo_barras) params.append('codigo_barras', filters.value.codigo_barras)
    if (filters.value.ativo !== 'todos') params.append('status', filters.value.ativo === 'ativo')
    if (filters.value.fornecedor_id) params.append('fornecedor_id', filters.value.fornecedor_id)
    
    params.append('page', currentPage.value)
    params.append('per_page', itemsPerPage.value)

    const response = await api.get('/produto/filtro', { params })
    
    produtos.value = response.data
    totalItems.value = response.headers['x-total-count'] || response.data.length
    totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value)
    
  } catch (err) {
    error.value = 'Erro ao carregar produtos'
    console.error('Erro:', err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    }
  } finally {
    loading.value = false
  }
}

// Buscar fornecedores da API
const fetchFornecedores = async () => {
  try {
    const response = await api.get('/fornecedor') // Ajuste esta rota conforme sua API
    fornecedores.value = response.data
  } catch (err) {
    console.error('Erro ao buscar fornecedores:', err)
  }
}

// Editar produto
const editProduto = (id) => {
  router.push(`/produtos/editar/${id}`)
}

// Inativar/Ativar produto
const toggleStatus = async (produto) => {
  if (!confirm(`Tem certeza que deseja ${produto.ativo ? 'inativar' : 'ativar'} este produto?`)) {
    return
  }

  try {
    await api.patch(`/produto/${produto.id}`)
    await fetchProdutos() // Recarrega a lista após a alteração
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
  filters,
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
              <CIcon name="cil-plus" /> Novo Produto
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
                <CTableHeaderCell>Descrição</CTableHeaderCell>
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
                <CTableDataCell>{{ produto.descricao || '-' }}</CTableDataCell>
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
                <CTableDataCell colspan="8" class="text-center">
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

<style scoped>
.product-list-wrapper {
  padding: 20px;
}
</style>