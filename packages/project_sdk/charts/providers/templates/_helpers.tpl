{{/*
Expand the name of the chart.
*/}}
{{- define "data-provider.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 40 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
If release name contains chart name it will be used as a full name.
*/}}
{{- define "data-provider.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 40 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 40 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 40 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Extract data-provider name from parent chart alias
This is crucial - the release name doesn't contain the data-provider name,
but we can extract it from the chart context since each data-provider is
deployed as a subchart with an alias that matches the data-provider name
*/}}
{{- define "data-provider.providerName" -}}
{{- .Chart.Name | replace "data-provider-" "" -}}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "data-provider.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 40 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "data-provider.labels" -}}
helm.sh/chart: {{ include "data-provider.chart" . }}
{{ include "data-provider.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "data-provider.selectorLabels" -}}
app.kubernetes.io/name: {{ include "data-provider.name" . | trunc 40 }}
app.kubernetes.io/instance: {{ .Release.Name | trunc 20 }}
app.kubernetes.io/component: {{ .Chart.Name }}
{{- end }}

{{/*
Ray service name
*/}}
{{- define "data-provider.rayServiceName" -}}
{{- printf "%s" .Chart.Name | trunc 50 | trimSuffix "-" }}
{{- end }}

{{/*
Ray head service name
*/}}
{{- define "data-provider.rayHeadServiceName" -}}
{{- printf "%s-head" (include "data-provider.rayServiceName" .) | trunc 55 | trimSuffix "-" }}
{{- end }}

{{/*
Ray worker group name
*/}}
{{- define "data-provider.rayWorkerGroupName" -}}
{{- printf "%s-workers" (include "data-provider.rayServiceName" .) | trunc 58 | trimSuffix "-" }}
{{- end }}

{{- /*
  generateServeConfigV2 creates the full serveConfigV2 structure with default values,
  using only the pipPackages provided by the user.
*/}}
{{- define "data-provider.serveConfigV2" -}}
http_options:
  host: 0.0.0.0
  port: 8000
applications:
- name: provider-app
  import_path: entrypoint:app
  route_prefix: "/api/v1"
  runtime_env:
    pip: {{ .Values.pip | default list | toYaml | nindent 6 }}
{{- end -}}
