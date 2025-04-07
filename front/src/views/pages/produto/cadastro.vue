<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Dados do produto
const produto = ref({
  codigo_interno: '',
  nome: '',
  descricao: '',
  preco: 0,
  estoque: 0,
  unidade_medida: 'un',
  marca: '',
  codigo_barras: '',
  ativo: true,
  fornecedor_id: null // Inicialmente null, será obrigatório
})

// Opções de unidades de medida
const unidadesMedida = [
  { value: 'un', label: 'Unidade' },
  { value: 'kg', label: 'Quilograma' },
  { value: 'g', label: 'Grama' },
  { value: 'l', label: 'Litro' },
  { value: 'ml', label: 'Mililitro' },
  { value: 'm', label: 'Metro' },
  { value: 'cm', label: 'Centímetro' },
  { value: 'cx', label: 'Caixa' },
  { value: 'pct', label: 'Pacote' }
]

// Estado de validação
const validated = ref(false)
const submitting = ref(false)
const errorMessage = ref('')


// Lista de fornecedores (simulada - você deve substituir pela sua chamada API)
const fornecedores = ref([
  { id: 1, nome: 'Fornecedor A' },
  { id: 2, nome: 'Fornecedor B' },
  { id: 3, nome: 'Fornecedor C' }
])

// Carrega fornecedores ao montar o componente
const loadFornecedores = async () => {
  try {
    // Substitua pela chamada real à sua API
    //const response = await axios.get('https://sua-api.com/fornecedores')
    //fornecedores.value = response.data
    console.log ('implementar chamada pra api!')
  } catch (error) {
    console.error('Erro ao carregar fornecedores:', error)
    errorMessage.value = 'Não foi possível carregar a lista de fornecedores'
  }
}

// Carrega fornecedores quando o componente é montado
loadFornecedores()

// Função para enviar o formulário
const handleSubmit = async (event) => {
  const form = event.currentTarget
  validated.value = true
  
  if (form.checkValidity() === false || !produto.value.fornecedor_id) {
    event.preventDefault()
    event.stopPropagation()
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    const response = await axios.post('https://sua-api.com/produtos', produto.value)
    router.push({ 
      name: 'produtos', 
      query: { 
        success: `Produto ${produto.value.nome} cadastrado com sucesso!` 
      } 
    })
  } catch (error) {
    console.error('Erro ao cadastrar produto:', error)
    errorMessage.value = error.response?.data?.message || 'Erro ao cadastrar produto'
  } finally {
    submitting.value = false
  }
}

// Máscara para preço
const formatPrice = (value) => {
  return parseFloat(value).toFixed(2)
}
</script>

<template>
  <div class="product-register-wrapper">
    <CContainer fluid>
      <CCard>
        <CCardHeader>
          <strong>Informações do Produto</strong>
        </CCardHeader>
        <CCardBody>
          <CAlert v-if="errorMessage" color="danger">{{ errorMessage }}</CAlert>

          <CForm
            class="row g-3 needs-validation"
            novalidate
            :validated="validated"
            @submit="handleSubmit"
          >
            <!-- Seção 1: Dados Básicos -->
            <CCol :md="6">
              <CFormLabel for="nome">Nome do Produto <span class="text-danger">*</span></CFormLabel>
              <CFormInput
                id="nome"
                v-model="produto.nome"
                placeholder="Digite o nome do produto"
                required
              />
              <CFormFeedback invalid>Por favor, informe o nome do produto</CFormFeedback>
            </CCol>

            <CCol :md="6">
              <CFormLabel for="codigo_interno">Código Interno</CFormLabel>
              <CFormInput
                id="codigo_interno"
                v-model="produto.codigo_interno"
                placeholder="Código interno do produto"
              />
            </CCol>

            <CCol :md="12">
              <CFormLabel for="descricao">Descrição</CFormLabel>
              <CFormTextarea
                id="descricao"
                v-model="produto.descricao"
                placeholder="Descrição detalhada do produto"
                rows="3"
              />
            </CCol>

            <!-- Seção 2: Preço e Estoque -->
            <CCol :md="4">
              <CFormLabel for="preco">Preço (R$) <span class="text-danger">*</span></CFormLabel>
              <CInputGroup>
                <CInputGroupText>R$</CInputGroupText>
                <CFormInput
                  id="preco"
                  v-model="produto.preco"
                  type="number"
                  min="0"
                  step="0.01"
                  required
                  @blur="produto.preco = formatPrice(produto.preco)"
                />
              </CInputGroup>
              <CFormFeedback invalid>Informe um preço válido</CFormFeedback>
            </CCol>

            <CCol :md="4">
              <CFormLabel for="estoque">Estoque <span class="text-danger">*</span></CFormLabel>
              <CFormInput
                id="estoque"
                v-model="produto.estoque"
                type="number"
                min="0"
                required
              />
              <CFormFeedback invalid>Informe a quantidade em estoque</CFormFeedback>
            </CCol>

            <CCol :md="4">
              <CFormLabel for="unidade_medida">Unidade de Medida <span class="text-danger">*</span></CFormLabel>
              <CFormSelect
                id="unidade_medida"
                v-model="produto.unidade_medida"
                required
              >
                <option v-for="unidade in unidadesMedida" :key="unidade.value" :value="unidade.value">
                  {{ unidade.label }} ({{ unidade.value }})
                </option>
              </CFormSelect>
            </CCol>

            <!-- Seção 3: Informações Adicionais -->
            <CCol :md="6">
              <CFormLabel for="marca">Marca</CFormLabel>
              <CFormInput
                id="marca"
                v-model="produto.marca"
                placeholder="Marca do produto"
              />
            </CCol>

            <CCol :md="6">
              <CFormLabel for="codigo_barras">Código de Barras</CFormLabel>
              <CFormInput
                id="codigo_barras"
                v-model="produto.codigo_barras"
                placeholder="Código de barras (EAN, UPC, etc)"
              />
            </CCol>

            <!-- Campo de Fornecedor (agora obrigatório) -->
            <CCol :md="6">
              <CFormLabel for="fornecedor_id">Fornecedor <span class="text-danger">*</span></CFormLabel>
              <CFormSelect
                id="fornecedor_id"
                v-model="produto.fornecedor_id"
                required
                :invalid="validated && !produto.fornecedor_id"
              >
                <option :value="null" disabled>Selecione um fornecedor...</option>
                <option 
                  v-for="fornecedor in fornecedores" 
                  :key="fornecedor.id" 
                  :value="fornecedor.id"
                >
                  {{ fornecedor.nome }}
                </option>
              </CFormSelect>
              <CFormFeedback v-if="validated && !produto.fornecedor_id" invalid>
                Por favor, selecione um fornecedor
              </CFormFeedback>
            </CCol>

            <CCol :md="6">
              <CFormLabel for="ativo">Status</CFormLabel>
              <div class="mt-2">
                <CSwitch
                  id="ativo"
                  v-model="produto.ativo"
                  color="primary"
                  :checked="produto.ativo"
                  label
                  :value="true"
                  :unchecked-value="false"
                >
                  {{ produto.ativo ? 'Ativo' : 'Inativo' }}
                </CSwitch>
              </div>
            </CCol>

            <!-- Botões de ação -->
            <CCol :xs="12" class="mt-4">
              <div class="d-flex justify-content-between">
                <CButton color="secondary" @click="router.push('/produtos')">
                  Cancelar
                </CButton>
                <CButton type="submit" color="primary" :disabled="submitting">
                  <CSpinner v-if="submitting" component="span" size="sm" aria-hidden="true" />
                  {{ submitting ? 'Salvando...' : 'Salvar Produto' }}
                </CButton>
              </div>
            </CCol>
          </CForm>
        </CCardBody>
      </CCard>
    </CContainer>
  </div>
</template>