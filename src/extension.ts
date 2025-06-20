import * as vscode from 'vscode';
import axios from 'axios';
import * as fs from 'fs';
import * as path from 'path';

// API 인터페이스 정의
interface CodeConversionRequest {
    source_code: string;
    target_language: string;
    source_language?: string;
    file_path?: string;
    start_line?: number;
    end_line?: number;
    additional_instructions?: string;
}

interface CodeConversionResponse {
    converted_code: string;
    source_language: string;
    target_language: string;
    file_path?: string;
    start_line?: number;
    end_line?: number;
    processing_time: number;
    success: boolean;
    message: string;
}

interface MakeVORequest {
    project_path: string;
    additional_instructions?: string;
}

interface MakeVOResponse {
    vo_code: string;
    file_count: number;
    processing_time: number;
    success: boolean;
    message: string;
}

// LLM API 클라이언트
class LLMCodeConverter {
    private apiEndpoint: string;
    private timeout: number;

    constructor() {
        const config = vscode.workspace.getConfiguration('llmCodeConverter');
        this.apiEndpoint = config.get('apiEndpoint', 'http://localhost:8000');
        this.timeout = config.get('timeout', 30000);
    }

    async convertCode(
        fullFileContent: string,
        targetLanguage: string,
        sourceLanguage?: string,
        filePath?: string,
        startLine?: number,
        endLine?: number
    ): Promise<CodeConversionResponse> {
        try {
            const request: CodeConversionRequest = {
                source_code: fullFileContent,
                target_language: targetLanguage,
                source_language: sourceLanguage,
                file_path: filePath,
                start_line: startLine,
                end_line: endLine
            };

            const response = await axios.post(`${this.apiEndpoint}/convert-code`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            return response.data;
        } catch (error) {
            throw new Error(`API request failed: ${error}`);
        }
    }

    async makeVO(projectPath: string): Promise<MakeVOResponse> {
        try {
            const request: MakeVORequest = {
                project_path: projectPath
            };

            const response = await axios.post(`${this.apiEndpoint}/make-vo`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            return response.data;
        } catch (error) {
            throw new Error(`Make VO API request failed: ${error}`);
        }
    }

    async checkHealth(): Promise<boolean> {
        try {
            const response = await axios.get(`${this.apiEndpoint}/health`, {
                timeout: 5000
            });
            return response.status === 200;
        } catch (error) {
            return false;
        }
    }
}

// 공통 아이템 클래스
class BaseItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly iconPath: string,
        public readonly description?: string,
        public readonly itemType?: string,
        public readonly commandId?: string
    ) {
        super(label, collapsibleState);
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
class VOGeneratorProvider implements vscode.TreeDataProvider<BaseItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<BaseItem | undefined | null | void> = new vscode.EventEmitter<BaseItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<BaseItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private projectPath: string = '';
    private outputPath: string = '';
    private analysisResult: string = 'No analysis performed yet';
    private fileCount: number = 0;
    private lastRunStatus: 'idle' | 'running' | 'success' | 'error' = 'idle';

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: BaseItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: BaseItem): Thenable<BaseItem[]> {
        if (!element) {
            return Promise.resolve([
                new BaseItem('📁 Project Path', vscode.TreeItemCollapsibleState.None, 'folder', 
                    this.projectPath || 'Click to set project path', 'project-path', 'llm-code-converter.setProjectPath'),
                new BaseItem('📂 Output Path', vscode.TreeItemCollapsibleState.None, 'folder-opened', 
                    this.outputPath || 'Click to set output path', 'output-path', 'llm-code-converter.setOutputPath'),
                new BaseItem('📊 File Count', vscode.TreeItemCollapsibleState.None, 'file', `${this.fileCount} files`),
                new BaseItem('🔄 Status', vscode.TreeItemCollapsibleState.None, this.getStatusIcon(), this.getStatusText()),
                new BaseItem('📋 Last Result', vscode.TreeItemCollapsibleState.Collapsed, 'output', this.analysisResult)
            ]);
        } else if (element.label === '📋 Last Result') {
            return Promise.resolve([
                new BaseItem(this.analysisResult, vscode.TreeItemCollapsibleState.None, 'info', '')
            ]);
        }
        return Promise.resolve([]);
    }

    private getStatusIcon(): string {
        switch (this.lastRunStatus) {
            case 'running': return 'loading~spin';
            case 'success': return 'check';
            case 'error': return 'error';
            default: return 'circle-outline';
        }
    }

    private getStatusText(): string {
        switch (this.lastRunStatus) {
            case 'running': return 'Running VO generation...';
            case 'success': return 'VO generation completed';
            case 'error': return 'VO generation failed';
            default: return 'Ready to generate VO';
        }
    }

    async setProjectPath(): Promise<void> {
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

    async setOutputPath(): Promise<void> {
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

    private countFiles(): void {
        if (!this.projectPath || !fs.existsSync(this.projectPath)) {
            this.fileCount = 0;
            return;
        }

        try {
            const files = this.getAllFiles(this.projectPath);
            this.fileCount = files.length;
        } catch (error) {
            this.fileCount = 0;
        }
    }

    private getAllFiles(dirPath: string): string[] {
        const files: string[] = [];
        try {
            const items = fs.readdirSync(dirPath);

            for (const item of items) {
                const fullPath = path.join(dirPath, item);
                const stat = fs.statSync(fullPath);

                if (stat.isDirectory()) {
                    if (!['node_modules', '.git', '.vscode', '__pycache__', 'out', 'dist'].includes(item)) {
                        files.push(...this.getAllFiles(fullPath));
                    }
                } else {
                    const ext = path.extname(item).toLowerCase();
                    if (['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.php'].includes(ext)) {
                        files.push(fullPath);
                    }
                }
            }
        } catch (error) {
            console.error('Error reading directory:', error);
        }

        return files;
    }

    async runAnalysis(): Promise<void> {
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
                
                vscode.window.showInformationMessage(
                    `VO generated successfully! Found ${result.file_count} files in ${result.processing_time.toFixed(2)}s`
                );
            } else {
                throw new Error(result.message);
            }

        } catch (error) {
            this.analysisResult = `Error: ${error}`;
            this.lastRunStatus = 'error';
            vscode.window.showErrorMessage(`VO generation failed: ${error}`);
        }

        this.refresh();
    }

    private async saveVOFile(voCode: string): Promise<void> {
        try {
            if (!fs.existsSync(this.outputPath)) {
                fs.mkdirSync(this.outputPath, { recursive: true });
            }

            const projectName = path.basename(this.projectPath).replace(/[^a-zA-Z0-9]/g, '_');
            const fileName = `${projectName}VO.java`;
            const filePath = path.join(this.outputPath, fileName);

            fs.writeFileSync(filePath, voCode, 'utf-8');

            vscode.window.showInformationMessage(`VO file saved to: ${filePath}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to save VO file: ${error}`);
        }
    }
}

// Code Converter Provider (두 번째 탭)
class CodeConverterProvider implements vscode.TreeDataProvider<BaseItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<BaseItem | undefined | null | void> = new vscode.EventEmitter<BaseItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<BaseItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private lastConversion: string = 'No conversion performed yet';
    private conversionHistory: string[] = [];
    private apiStatus: 'unknown' | 'online' | 'offline' = 'unknown';

    refresh(): void {
        this.checkAPIStatus();
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: BaseItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: BaseItem): Thenable<BaseItem[]> {
        if (!element) {
            return Promise.resolve([
                new BaseItem('🌐 API Status', vscode.TreeItemCollapsibleState.None, this.getAPIStatusIcon(), this.getAPIStatusText()),
                // new BaseItem('🔄 Convert Selection', vscode.TreeItemCollapsibleState.None, 'arrow-right', 'Drag and convert code to #', 'convert', 'llm-code-converter.convertCode'),
                new BaseItem('🔄 Convert Selection', vscode.TreeItemCollapsibleState.None, 'arrow-right', 'Drag and convert code  Map to VO', 'convert', 'llm-code-converter.convertCode'),
                new BaseItem('📝 Last Conversion', vscode.TreeItemCollapsibleState.None, 'file-text', this.lastConversion),
                new BaseItem('📚 History', vscode.TreeItemCollapsibleState.Collapsed, 'history', `${this.conversionHistory.length} conversions`),
                new BaseItem('⚙️ Settings', vscode.TreeItemCollapsibleState.Collapsed, 'gear', 'API configuration')
            ]);
        } else if (element.label === '📚 History') {
            return Promise.resolve(
                this.conversionHistory.slice(-5).reverse().map((item, index) => 
                    new BaseItem(`${index + 1}. ${item}`, vscode.TreeItemCollapsibleState.None, 'file', '')
                )
            );
        } else if (element.label === '⚙️ Settings') {
            const config = vscode.workspace.getConfiguration('llmCodeConverter');
            return Promise.resolve([
                new BaseItem('API Endpoint', vscode.TreeItemCollapsibleState.None, 'link', config.get('apiEndpoint', 'http://localhost:8000')),
                new BaseItem('Timeout', vscode.TreeItemCollapsibleState.None, 'clock', `${config.get('timeout', 30000)}ms`)
            ]);
        }
        return Promise.resolve([]);
    }

    private async checkAPIStatus(): Promise<void> {
        try {
            const converter = new LLMCodeConverter();
            const isHealthy = await converter.checkHealth();
            this.apiStatus = isHealthy ? 'online' : 'offline';
        } catch (error) {
            this.apiStatus = 'offline';
        }
    }

    private getAPIStatusIcon(): string {
        switch (this.apiStatus) {
            case 'online': return 'check';
            case 'offline': return 'error';
            default: return 'question';
        }
    }

    private getAPIStatusText(): string {
        switch (this.apiStatus) {
            case 'online': return 'API Server Online';
            case 'offline': return 'API Server Offline';
            default: return 'Checking API...';
        }
    }

    addConversionHistory(description: string): void {
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

            const result = await converter.convertCode(
                fullFileContent,
                targetLanguage,
                undefined,
                filePath,
                startLine,
                endLine
            );

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
                
                vscode.window.showInformationMessage(
                    `Lines ${startLine}-${endLine} converted to # symbols!`
                );
            } else {
                vscode.window.showErrorMessage(`Conversion failed: ${result.message}`);
            }
        });
    } catch (error) {
        vscode.window.showErrorMessage(`Conversion failed: ${error}`);
    }
}

// 전역 변수로 provider 참조 저장
let voGeneratorProvider: VOGeneratorProvider;
let codeConverterProvider: CodeConverterProvider;

export function activate(context: vscode.ExtensionContext) {
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
    context.subscriptions.push(
        convertCodeDisposable, 
        generateVODisposable,
        refreshViewDisposable,
        refreshConverterDisposable,
        setProjectPathDisposable,
        setOutputPathDisposable,
        voTreeView,
        converterTreeView
    );

    console.log('✅ LLM Code Converter extension successfully activated!');
    vscode.window.showInformationMessage('LLM Code Converter is ready!');
}

export function deactivate() {
    console.log('👋 LLM Code Converter extension deactivated!');
}