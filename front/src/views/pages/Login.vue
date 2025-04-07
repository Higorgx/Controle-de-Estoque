<script setup>
import logo from '@/assets/icons/Logo.svg'

</script>
<template>
  <div class="wrapper min-vh-100 d-flex flex-row align-items-center">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol :md="10">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody style="max-width: 776px; margin: 0 auto;"> <!-- Adicionei max-width e margin auto -->
                <div class="d-flex flex-md-row flex-column align-items-md-center align-items-center mb-4">
                  <div class="text-center text-md-start mb-3 mb-md-0">
                    <img :src="logo" style="max-width: 120px; height: auto;">
                  </div>
                  
                  <div class="ms-md-4 w-100">
                    <h1 class="mb-0 text-center text-md-start">Login</h1>
                    <p class="text-body-secondary text-center text-md-start">Entre na sua conta</p>
                    
                    <CForm>
                      <CInputGroup class="mb-3">
                        <CInputGroupText>
                          <CIcon icon="cil-user" />
                        </CInputGroupText>
                        <CFormInput
                          placeholder="Username"
                          autocomplete="username"
                        />
                      </CInputGroup>
                      <CInputGroup class="mb-4">
                        <CInputGroupText>
                          <CIcon icon="cil-lock-locked" />
                        </CInputGroupText>
                        <CFormInput
                          type="password"
                          placeholder="Password"
                          autocomplete="current-password"
                        />
                      </CInputGroup>
                      <CRow>
                        <CCol :xs="6">
                          <CButton color="primary" class="px-4 w-100"> Login </CButton>
                        </CCol>
                        <CCol :xs="6" class="text-right">
                          <CButton color="link" class="px-0 w-100 text-md-end">
                            Forgot password?
                          </CButton>
                        </CCol>
                      </CRow>
                    </CForm>
                  </div>
                </div>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>