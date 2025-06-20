"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const axios_1 = __importDefault(require("axios"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
// LLM API 클라이언트
class LLMCodeConverter {
    constructor() {
        const config = vscode.workspace.getConfiguration('llmCodeConverter');
        this.apiEndpoint = config.get('apiEndpoint', 'http://localhost:8000');
        this.timeout = config.get('timeout', 30000);
    }
    async convertCode(fullFileContent, targetLanguage, sourceLanguage, filePath, startLine, endLine) {
        try {
            const request = {
                source_code: fullFileContent,
                target_language: targetLanguage,
                source_language: sourceLanguage,
                file_path: filePath,
                start_line: startLine,
                end_line: endLine
            };
            const response = await axios_1.default.post(`${this.apiEndpoint}/convert-code`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return response.data;
        }
        catch (error) {
            throw new Error(`API request failed: ${error}`);
        }
    }
    async makeVO(projectPath) {
        try {
            const request = {
                project_path: projectPath
            };
            const response = await axios_1.default.post(`${this.apiEndpoint}/make-vo`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return response.data;
        }
        catch (error) {
            throw new Error(`Make VO API request failed: ${error}`);
        }
    }
    async checkHealth() {
        try {
            const response = await axios_1.default.get(`${this.apiEndpoint}/health`, {
                timeout: 5000
            });
            return response.status === 200;
        }
        catch (error) {
            return false;
        }
    }
}
// 공통 아이템 클래스
class BaseItem extends vscode.TreeItem {
    constructor(label, collapsibleState, iconPath, description, itemType, commandId) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.iconPath = iconPath;
        this.description = description;
        this.itemType = itemType;
        this.commandId = commandId;
        this.tooltip = `${this.label}: ${this.description}`;
        this.description = description;
        if (commandId) {
            this.command = {
                command: commandId,
                title: this.label
            };
        }
    }
}
// VO Generator Provider (첫 번째 탭)
class VOGeneratorProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.projectPath = '';
        this.outputPath = '';
        this.analysisResult = 'No analysis performed yet';
        this.fileCount = 0;
        this.lastRunStatus = 'idle';
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            return Promise.resolve([
                new BaseItem('📁 Project Path', vscode.TreeItemCollapsibleState.None, 'folder', this.projectPath || 'Click to set project path', 'project-path', 'llm-code-converter.setProjectPath'),
                new BaseItem('📂 Output Path', vscode.TreeItemCollapsibleState.None, 'folder-opened', this.outputPath || 'Click to set output path', 'output-path', 'llm-code-converter.setOutputPath'),
                new BaseItem('📊 File Count', vscode.TreeItemCollapsibleState.None, 'file', `${this.fileCount} files`),
                new BaseItem('🔄 Status', vscode.TreeItemCollapsibleState.None, this.getStatusIcon(), this.getStatusText()),
                new BaseItem('📋 Last Result', vscode.TreeItemCollapsibleState.Collapsed, 'output', this.analysisResult)
            ]);
        }
        else if (element.label === '📋 Last Result') {
            return Promise.resolve([
                new BaseItem(this.analysisResult, vscode.TreeItemCollapsibleState.None, 'info', '')
            ]);
        }
        return Promise.resolve([]);
    }
    getStatusIcon() {
        switch (this.lastRunStatus) {
            case 'running': return 'loading~spin';
            case 'success': return 'check';
            case 'error': return 'error';
            default: return 'circle-outline';
        }
    }
    getStatusText() {
        switch (this.lastRunStatus) {
            case 'running': return 'Running VO generation...';
            case 'success': return 'VO generation completed';
            case 'error': return 'VO generation failed';
            default: return 'Ready to generate VO';
        }
    }
    async setProjectPath() {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter project path for VO generation',
            value: this.projectPath || vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '',
            placeHolder: '/path/to/your/project'
        });
        if (result) {
            this.projectPath = result;
            this.countFiles();
            this.refresh();
        }
    }
    async setOutputPath() {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter output path for generated VO files',
            value: this.outputPath || (this.projectPath ? path.join(this.projectPath, 'generated') : ''),
            placeHolder: '/path/to/output/directory'
        });
        if (result) {
            this.outputPath = result;
            this.refresh();
        }
    }
    countFiles() {
        if (!this.projectPath || !fs.existsSync(this.projectPath)) {
            this.fileCount = 0;
            return;
        }
        try {
            const files = this.getAllFiles(this.projectPath);
            this.fileCount = files.length;
        }
        catch (error) {
            this.fileCount = 0;
        }
    }
    getAllFiles(dirPath) {
        const files = [];
        try {
            const items = fs.readdirSync(dirPath);
            for (const item of items) {
                const fullPath = path.join(dirPath, item);
                const stat = fs.statSync(fullPath);
                if (stat.isDirectory()) {
                    if (!['node_modules', '.git', '.vscode', '__pycache__', 'out', 'dist'].includes(item)) {
                        files.push(...this.getAllFiles(fullPath));
                    }
                }
                else {
                    const ext = path.extname(item).toLowerCase();
                    if (['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.php'].includes(ext)) {
                        files.push(fullPath);
                    }
                }
            }
        }
        catch (error) {
            console.error('Error reading directory:', error);
        }
        return files;
    }
    async runAnalysis() {
        if (!this.projectPath) {
            vscode.window.showErrorMessage('Please set project path first');
            return;
        }
        if (!fs.existsSync(this.projectPath)) {
            vscode.window.showErrorMessage('Project path does not exist');
            return;
        }
        if (!this.outputPath) {
            vscode.window.showErrorMessage('Please set output path first');
            return;
        }
        this.lastRunStatus = 'running';
        this.refresh();
        try {
            const converter = new LLMCodeConverter();
            const isHealthy = await converter.checkHealth();
            if (!isHealthy) {
                throw new Error('LLM API is not available. Please check if the server is running.');
            }
            const result = await converter.makeVO(this.projectPath);
            if (result.success) {
                this.fileCount = result.file_count;
                this.analysisResult = `VO generated successfully!\nProject: ${this.projectPath}\nOutput: ${this.outputPath}\nFiles: ${result.file_count}\nTime: ${result.processing_time.toFixed(2)}s`;
                this.lastRunStatus = 'success';
                await this.saveVOFile(result.vo_code);
                const doc = await vscode.workspace.openTextDocument({
                    content: result.vo_code,
                    language: 'java'
                });
                await vscode.window.showTextDocument(doc);
                vscode.window.showInformationMessage(`VO generated successfully! Found ${result.file_count} files in ${result.processing_time.toFixed(2)}s`);
            }
            else {
                throw new Error(result.message);
            }
        }
        catch (error) {
            this.analysisResult = `Error: ${error}`;
            this.lastRunStatus = 'error';
            vscode.window.showErrorMessage(`VO generation failed: ${error}`);
        }
        this.refresh();
    }
    async saveVOFile(voCode) {
        try {
            if (!fs.existsSync(this.outputPath)) {
                fs.mkdirSync(this.outputPath, { recursive: true });
            }
            const projectName = path.basename(this.projectPath).replace(/[^a-zA-Z0-9]/g, '_');
            const fileName = `${projectName}VO.java`;
            const filePath = path.join(this.outputPath, fileName);
            fs.writeFileSync(filePath, voCode, 'utf-8');
            vscode.window.showInformationMessage(`VO file saved to: ${filePath}`);
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to save VO file: ${error}`);
        }
    }
}
// Code Converter Provider (두 번째 탭)
class CodeConverterProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.lastConversion = 'No conversion performed yet';
        this.conversionHistory = [];
        this.apiStatus = 'unknown';
    }
    refresh() {
        this.checkAPIStatus();
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            return Promise.resolve([
                new BaseItem('🌐 API Status', vscode.TreeItemCollapsibleState.None, this.getAPIStatusIcon(), this.getAPIStatusText()),
                // new BaseItem('🔄 Convert Selection', vscode.TreeItemCollapsibleState.None, 'arrow-right', 'Drag and convert code to #', 'convert', 'llm-code-converter.convertCode'),
                new BaseItem('🔄 Convert Selection', vscode.TreeItemCollapsibleState.None, 'arrow-right', 'Drag and convert code  Map to VO', 'convert', 'llm-code-converter.convertCode'),
                new BaseItem('📝 Last Conversion', vscode.TreeItemCollapsibleState.None, 'file-text', this.lastConversion),
                new BaseItem('📚 History', vscode.TreeItemCollapsibleState.Collapsed, 'history', `${this.conversionHistory.length} conversions`),
                new BaseItem('⚙️ Settings', vscode.TreeItemCollapsibleState.Collapsed, 'gear', 'API configuration')
            ]);
        }
        else if (element.label === '📚 History') {
            return Promise.resolve(this.conversionHistory.slice(-5).reverse().map((item, index) => new BaseItem(`${index + 1}. ${item}`, vscode.TreeItemCollapsibleState.None, 'file', '')));
        }
        else if (element.label === '⚙️ Settings') {
            const config = vscode.workspace.getConfiguration('llmCodeConverter');
            return Promise.resolve([
                new BaseItem('API Endpoint', vscode.TreeItemCollapsibleState.None, 'link', config.get('apiEndpoint', 'http://localhost:8000')),
                new BaseItem('Timeout', vscode.TreeItemCollapsibleState.None, 'clock', `${config.get('timeout', 30000)}ms`)
            ]);
        }
        return Promise.resolve([]);
    }
    async checkAPIStatus() {
        try {
            const converter = new LLMCodeConverter();
            const isHealthy = await converter.checkHealth();
            this.apiStatus = isHealthy ? 'online' : 'offline';
        }
        catch (error) {
            this.apiStatus = 'offline';
        }
    }
    getAPIStatusIcon() {
        switch (this.apiStatus) {
            case 'online': return 'check';
            case 'offline': return 'error';
            default: return 'question';
        }
    }
    getAPIStatusText() {
        switch (this.apiStatus) {
            case 'online': return 'API Server Online';
            case 'offline': return 'API Server Offline';
            default: return 'Checking API...';
        }
    }
    addConversionHistory(description) {
        const timestamp = new Date().toLocaleTimeString();
        this.conversionHistory.push(`${timestamp}: ${description}`);
        this.lastConversion = description;
        this.refresh();
    }
}
// 코드 변환 명령 (드래그한 부분을 #으로 변환)
async function convertCodeCommand() {
    const converter = new LLMCodeConverter();
    // API 헬스 체크
    const isHealthy = await converter.checkHealth();
    if (!isHealthy) {
        vscode.window.showErrorMessage('LLM API is not available. Please check if the server is running.');
        return;
    }
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }
    const selection = editor.selection;
    if (selection.isEmpty) {
        // vscode.window.showErrorMessage('Please select the code you want to convert to #');
        vscode.window.showErrorMessage('Please select the code you want to convert Map to VO');
        return;
    }
    const fullFileContent = editor.document.getText();
    const startLine = selection.start.line + 1;
    const endLine = selection.end.line + 1;
    const filePath = editor.document.fileName;
    if (!fullFileContent.trim()) {
        vscode.window.showErrorMessage('No file content');
        return;
    }
    const targetLanguage = '#';
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Converting code to # symbols...',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 50, message: 'Processing...' });
            const result = await converter.convertCode(fullFileContent, targetLanguage, undefined, filePath, startLine, endLine);
            progress.report({ increment: 50, message: 'Creating new document...' });
            if (result.success) {
                const doc = await vscode.workspace.openTextDocument({
                    content: result.converted_code,
                    language: 'plaintext'
                });
                await vscode.window.showTextDocument(doc);
                // 히스토리에 추가
                if (codeConverterProvider) {
                    codeConverterProvider.addConversionHistory(`Lines ${startLine}-${endLine} → # symbols`);
                }
                vscode.window.showInformationMessage(`Lines ${startLine}-${endLine} converted to # symbols!`);
            }
            else {
                vscode.window.showErrorMessage(`Conversion failed: ${result.message}`);
            }
        });
    }
    catch (error) {
        vscode.window.showErrorMessage(`Conversion failed: ${error}`);
    }
}
// 전역 변수로 provider 참조 저장
let voGeneratorProvider;
let codeConverterProvider;
function activate(context) {
    console.log('🚀 LLM Code Converter extension is now active!');
    // Provider 생성
    voGeneratorProvider = new VOGeneratorProvider();
    codeConverterProvider = new CodeConverterProvider();
    // 코드 변환 명령 등록 (드래그 -> #)
    const convertCodeDisposable = vscode.commands.registerCommand('llm-code-converter.convertCode', convertCodeCommand);
    // VO 생성 명령 등록
    const generateVODisposable = vscode.commands.registerCommand('llm-code-converter.generateVO', () => {
        voGeneratorProvider.runAnalysis();
    });
    // 새로고침 명령들 등록
    const refreshViewDisposable = vscode.commands.registerCommand('llm-code-converter.refreshView', () => {
        voGeneratorProvider.refresh();
    });
    const refreshConverterDisposable = vscode.commands.registerCommand('llm-code-converter.refreshConverter', () => {
        codeConverterProvider.refresh();
    });
    // 경로 설정 명령들 등록
    const setProjectPathDisposable = vscode.commands.registerCommand('llm-code-converter.setProjectPath', () => {
        voGeneratorProvider.setProjectPath();
    });
    const setOutputPathDisposable = vscode.commands.registerCommand('llm-code-converter.setOutputPath', () => {
        voGeneratorProvider.setOutputPath();
    });
    // Tree View들 등록 (탭으로 분리됨)
    const voTreeView = vscode.window.createTreeView('voGeneratorView', {
        treeDataProvider: voGeneratorProvider,
        showCollapseAll: true
    });
    const converterTreeView = vscode.window.createTreeView('codeConverterView', {
        treeDataProvider: codeConverterProvider,
        showCollapseAll: true
    });
    // 구독에 추가
    context.subscriptions.push(convertCodeDisposable, generateVODisposable, refreshViewDisposable, refreshConverterDisposable, setProjectPathDisposable, setOutputPathDisposable, voTreeView, converterTreeView);
    console.log('✅ LLM Code Converter extension successfully activated!');
    vscode.window.showInformationMessage('LLM Code Converter is ready!');
}
exports.activate = activate;
function deactivate() {
    console.log('👋 LLM Code Converter extension deactivated!');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map