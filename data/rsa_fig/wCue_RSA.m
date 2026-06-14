%% RSA ROI
% Compute Tau
% by Jin Liu 1.Oct.2023

clear;
close all;
clc;

%% Setting
fs=filesep;
Respath='E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\wCue_RSA'; %save path
RDMpath='E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\wCue_RSA';% RSA results path 

ROIs={'Amyl','Amyr','ECl','ECr','HCl', 'HCr','mPFC'};% Anatomically defined ROIs;
% ROIs={'HCl'}
Nperm=1000; % num permutation, 1000 
nsubj=24;

%%%%%%%%%%%%%%%%%%%%%%%%% User Inputs %%%%%%%%%%%%%%%%%%%%%%%%% 
% wCue faceNum=28 
Face=[10,11,12,13,14,15,2,3,4,5,6,7,8,9,10,11,12,13,14,15,2,3,4,5,6,7,8,9];
RB=[ones(1,14),2*ones(1,14)];
rng=Face;
svoption=0; % 1 if you want to save the results of RDM as mat file. 0 otherwise.
svfile='Results_TauA'; %savefile name
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% rbCue EDI
[E_rdm,E_rdm_perm]=EucRDM(rng, Nperm); % 14张面孔的二维E距离
[D1_rdm, D2_rdm, D1_rdm_perm,D2_rdm_perm]=DI_RDM_rbCue(rng, RB, Nperm);% 28张面孔的D I距离 D1表示D D2表示I 
[Diag_rdm,Diag_rdm_perm]=DI_RDM(rng,3, Nperm); % 28张面孔的diag距离
fprintf('\n %s   ');

% Load RDM generated from RDM
svpath=[Respath, fs]; % Save path
if exist(fullfile([RDMpath, fs], ['wCue_RDM','.mat']),'file')
    load(fullfile([RDMpath, fs], ['wCue_RDM','.mat'])); % Where the RDM is; Load RDM (cross blocks)
else
    error('The RDM is missing');
end
        
    for r=1:numel(ROIs)
    fprintf('\n %s   ', ROIs{r});
        for s=1:nsubj
            fprintf('%d   ', s);
            RDMroisub=[squeeze(MDS.(ROIs{r}).RDM(s,:,:)),squeeze(MDS.(ROIs{r}).RDM(s,:,:));squeeze(MDS.(ROIs{r}).RDM(s,:,:)),squeeze(MDS.(ROIs{r}).RDM(s,:,:))];
    %% Rank correation of Euclidean distances and two 1-D distances in each of two social hierarchy dimensions       
            tauEach.Ec0(s)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(E_rdm) ); % with pairwise Euclidean distance model
            tauEach.Diagc0(s)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(Diag_rdm) ); % with rank distandce in the diag distance
            tauEach.D1c0(s)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(D1_rdm) ); % with rank distandce in the Dimension 1
            tauEach.D2c0(s)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(D2_rdm) ); % with rank distandce in the Dimension 2

    %% Computing permuted baseline
        %  Compute the Kendall's tau based on the permuted baseline
            for np=1:Nperm 
                tauEach.permE(s,np)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub),selectriu(E_rdm_perm{np}));
                tauEach.permDiag(s,np)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(Diag_rdm_perm{np}) );
                tauEach.permD1(s,np)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(D1_rdm_perm{np}) );
                tauEach.permD2(s,np)=rsa.stat.rankCorr_Kendall_taua(selectriu(RDMroisub), selectriu(D2_rdm_perm{np}) );    
            end
    % Correct according to the permuated baseline 
            tauEach.E(s)=tauEach.Ec0(s)-mean(tauEach.permE(s,:));
            tauEach.Diag(s)=tauEach.Diagc0(s)-mean(tauEach.permDiag(s,:));
            tauEach.D1(s)=tauEach.D1c0(s)-mean(tauEach.permD1(s,:));
            tauEach.D2(s)=tauEach.D2c0(s)-mean(tauEach.permD2(s,:));

        end %for subject s

    %% One-sample Wilcoxon signrank test 
             [p.E(r), ~]=rsa.stat.signrank_onesided(tauEach.E);
             [p.Diag(r), ~]=rsa.stat.signrank_onesided(tauEach.Diag);
             [p.D1(r), ~]=rsa.stat.signrank_onesided(tauEach.D1);
             [p.D2(r), ~]=rsa.stat.signrank_onesided(tauEach.D2);
             
%              [p.E(r), ~]=signrank(tauEach.E);
%              [p.Diag(r), ~]=signrank(tauEach.Diag);
%              [p.D1(r), ~]=signrank(tauEach.D1);
%              [p.D2(r), ~]=signrank(tauEach.D2);
             
    % for Figures (Boxplot)         
             tau.(ROIs{r}).meanD1=mean(tauEach.D1);
             tau.(ROIs{r}).meanD2=mean(tauEach.D2);
             tau.(ROIs{r}).meanDiag=mean(tauEach.Diag);
             tau.(ROIs{r}).meanE=mean(tauEach.E);
             tau.(ROIs{r}).D1=tauEach.D1';
             tau.(ROIs{r}).D2=tauEach.D2';
             tau.(ROIs{r}).Diag=tauEach.Diag';
             tau.(ROIs{r}).E=tauEach.E';
             tau.(ROIs{r}).seD1=SEM(tauEach.D1');
             tau.(ROIs{r}).seD2=SEM(tauEach.D2');
             tau.(ROIs{r}).seDiag=SEM(tauEach.Diag');
             tau.(ROIs{r}).seE=SEM(tauEach.E');
             tau.(ROIs{r}).tauRaw=tauEach;

      %% Comparion (E vs. D1; E vs. D2; E vs. Diag; D1 vs. D2; D1 vs. Diag; Diag vs. D2).
        % Paired signrank test
         [p.DiagE(r), h.DiagE(r), stats.DiagE(r)]=signrank(tauEach.Diag',tauEach.E');
         [p.DiagD1(r), h.DiagD1(r), stats.DiagD1(r)]=signrank(tauEach.Diag',tauEach.D1');
         [p.DiagD2(r), h.DiagD2(r), stats.DiagD2(r)]=signrank(tauEach.Diag',tauEach.D2');
         [p.ED1(r), h.ED1(r), stats.ED1(r)]=signrank(tauEach.E', tauEach.D1');
         [p.ED2(r), h.ED2(r), stats.ED2(r)]=signrank(tauEach.E', tauEach.D2');
         [p.D1D2(r), h.D1D2(r), stats.D1D2(r)]=signrank(tauEach.D1', tauEach.D2'); 
             
             
    end %for ROIs r

    %% Save results to mat
    tau.All.p=p;
    tau.All.h=h;
    tau.All.stats=stats;

    if svoption
        save(fullfile(svpath, [svfile, '.mat']), 'tau','Nperm','ROIs');
    end
    tau_allModels=tau;
    
    
     %% Figures
    % 准备绘图
    tau.All.E=[]; tau.All.E_mean=[]; tau.All.E_se=[]; 
    tau.All.Diag=[]; tau.All.Diag_mean=[]; tau.All.Diag_se=[];
    tau.All.D1=[]; tau.All.D1_mean=[]; tau.All.D1_se=[]; 
    tau.All.D2=[]; tau.All.D2_mean=[]; tau.All.D2_se=[]; 
    for r=1:numel(ROIs)
        tau.All.E=[tau.All.E, tau.(ROIs{r}).E];
        tau.All.Diag=[tau.All.Diag, tau.(ROIs{r}).Diag];
        tau.All.D1=[tau.All.D1, tau.(ROIs{r}).D1];
        tau.All.D2=[tau.All.D2, tau.(ROIs{r}).D2];

        tau.All.E_mean=[tau.All.E_mean, tau.(ROIs{r}).meanE];
        tau.All.Diag_mean=[tau.All.Diag_mean, tau.(ROIs{r}).meanDiag];
        tau.All.D1_mean=[tau.All.D1_mean, tau.(ROIs{r}).meanD1];
        tau.All.D2_mean=[tau.All.D2_mean, tau.(ROIs{r}).meanD2];

        tau.All.E_se=[tau.All.E_se, tau.(ROIs{r}).seE];
        tau.All.Diag_se=[tau.All.Diag_se, tau.(ROIs{r}).seDiag];
        tau.All.D1_se=[tau.All.D1_se, tau.(ROIs{r}).seD1];
        tau.All.D2_se=[tau.All.D2_se, tau.(ROIs{r}).seD2]; 
        
    end
    % holm-corrected
    % 假设有多个假设检验需要进行，每个检验的 p 值存储在一个向量中[raw_data] 
    % holm-corrected 每种比较（包含自身的四个基本模型以及六个比较的模型）都是基于7个ROI做的校正
    % 1. 对 p 值进行排序，并记录排序后的索引
    [sorted_p_Diag, p_Diag_index] = sort(tau.All.p.Diag);
    [sorted_p_E, p_E_index] = sort(tau.All.p.E);
    [sorted_p_D1, p_D1_index] = sort(tau.All.p.D1);
    [sorted_p_D2, p_D2_index] = sort(tau.All.p.D2);
    [sorted_p_DiagE, p_DiagE_index] = sort(tau.All.p.DiagE);
    [sorted_p_DiagD1, p_DiagD1_index] = sort(tau.All.p.DiagD1);
    [sorted_p_DiagD2, p_DiagD2_index] = sort(tau.All.p.DiagD2);
    [sorted_p_ED1, p_ED1_index] = sort(tau.All.p.ED1);
    [sorted_p_ED2, p_ED2_index] = sort(tau.All.p.ED2);
    [sorted_p_D1D2, p_D1D2_index] = sort(tau.All.p.D1D2);

    % 2. 使用Bonferroni-Holm方法对排序后的 p 值进行校正
    corrected_p_Diag = zeros(size(tau.All.p.Diag)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.Diag)
        corrected_p_Diag(p_Diag_index(i)) = min(1, sorted_p_Diag(i) * (numel(tau.All.p.Diag) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_E = zeros(size(tau.All.p.E)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.E)
        corrected_p_E(p_E_index(i)) = min(1, sorted_p_E(i) * (numel(tau.All.p.E) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_D1 = zeros(size(tau.All.p.D1)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.D1)
        corrected_p_D1(p_D1_index(i)) = min(1, sorted_p_D1(i) * (numel(tau.All.p.D1) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_D2 = zeros(size(tau.All.p.D2)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.D2)
        corrected_p_D2(p_D2_index(i)) = min(1, sorted_p_D2(i) * (numel(tau.All.p.D2) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_DiagE = zeros(size(tau.All.p.DiagE)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.DiagE)
        corrected_p_DiagE(p_DiagE_index(i)) = min(1, sorted_p_DiagE(i) * (numel(tau.All.p.DiagE) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_DiagD1 = zeros(size(tau.All.p.DiagD1)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.DiagD1)
        corrected_p_DiagD1(p_DiagD1_index(i)) = min(1, sorted_p_DiagD1(i) * (numel(tau.All.p.DiagD1) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_DiagD2 = zeros(size(tau.All.p.DiagD2)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.DiagD2)
        corrected_p_DiagD2(p_DiagD2_index(i)) = min(1, sorted_p_DiagD2(i) * (numel(tau.All.p.DiagD2) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_ED1 = zeros(size(tau.All.p.ED1)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.ED1)
        corrected_p_ED1(p_ED1_index(i)) = min(1, sorted_p_ED1(i) * (numel(tau.All.p.ED1) + 1 - i)); % 校正后的 p 值
    end

    corrected_p_ED2 = zeros(size(tau.All.p.ED2)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.ED2)
        corrected_p_ED2(p_ED2_index(i)) = min(1, sorted_p_ED2(i) * (numel(tau.All.p.ED2) + 1 - i)); % 校正后的 p 值
    end
    
    corrected_p_D1D2 = zeros(size(tau.All.p.D1D2)); % 用于记录校正后的 p 值
    for i = 1:numel(tau.All.p.D1D2)
        corrected_p_D1D2(p_D1D2_index(i)) = min(1, sorted_p_D1D2(i) * (numel(tau.All.p.D1D2) + 1 - i)); % 校正后的 p 值
    end    
    
    % 3、输出校正后的 p 值
    P.only = [corrected_p_Diag;corrected_p_E;corrected_p_D1;corrected_p_D2];
    P.DiagE  = corrected_p_DiagE;
    P.DiagD1  = corrected_p_DiagD1;
    P.DiagD2  = corrected_p_DiagD2;
    P.ED1  = corrected_p_ED1;
    P.ED2  = corrected_p_ED2;
    P.D1D2  = corrected_p_D1D2;
   
   
    clear fig
	% Fig1. TauA for Diag E and two 1D RDM
        i=1;  
        pos = [-.2+(i-1*.3) .2 .55 .20];
        set(gcf, 'Color', ones(1,3),'Units', 'Normalized', 'Position', pos);
        fig(i)=figure;
        xlables = repmat(ROIs,1,4); 
        simobs = [repmat({'Diag'},1,7),repmat({'E'},1,7),repmat({'D'},1,7),repmat({'I'},1,7)];
        boxplot([tau.All.Diag,tau.All.E,tau.All.D1,tau.All.D2],{xlables,simobs},'colors',repmat('bkrg',1,10),'factorgap',[5 2],'labelverbosity','minor');
%       patch
        boxobj = findobj(gca,'Tag','Box');
        colorGps = repmat('grkb',1,7);
        for i = 1:length(boxobj)
            patch(get(boxobj(i),'XData'),get(boxobj(i),'YData'), colorGps(i), 'FaceAlpha', 0.5);
        end
        set(findobj(gca,'Type','text'),'FontSize',15,'FontWeight','bold','VerticalAlignment', 'Middle')
        set(gca, 'Fontsize', 15,'FontWeight','bold');
        hold on;
        line([0,100],[0,0],'linestyle','--','color','black')
        ylim([-0.1,0.24])
        pos=[1:1.54:5.62, 7.98:1.54:12.62, 14.97:1.54:19.62, 21.94:1.54:26.62, 28.85:1.54:33.62, 35.85:1.54:40.62, 42.85:1.54:47.62];

% % % % % %  绘制显著行标记 % % % % % %  
        P.y=0.18;
        % 本身线
        for i=1:28
            x1=pos(i);x2=pos(i);
            sigline([x1,x2],P.y,P.only(i));
        end
        % DiagE
        j=1;
        for i=1:4:28
            x1=pos(i);x2=pos(i+1);
            sigline([x1,x2],P.y+0.015,P.DiagE(j));
            j=j+1;
        end
        
        % ED1
        j=1;
        for i=2:4:28
            x1=pos(i);x2=pos(i+1);
            sigline([x1,x2],P.y+0.017,P.ED1(j));
            j=j+1;
        end
        
        % D1D2
        j=1;
        for i=3:4:28
            x1=pos(i);x2=pos(i+1);
            sigline([x1,x2],P.y+0.015,P.D1D2(j));
            j=j+1;
        end
        
        % DiagD1
        j=1;
        for i=1:4:28
            x1=pos(i);x2=pos(i+2);
            sigline([x1,x2],P.y+0.032,P.DiagD1(j));
            j=j+1;
        end
        
        % ED2
        j=1;
        for i=2:4:28
            x1=pos(i);x2=pos(i+2);
            sigline([x1,x2],P.y+0.034,P.ED2(j));
            j=j+1;
        end

      % DiagD2
        j=1;
        for i=1:4:28
            x1=pos(i);x2=pos(i+3);
            sigline([x1,x2],P.y+0.049,P.DiagD2(j));
            j=j+1;
        end
        
        title('Tau_A for Diag E, D and I (wCue)');
        hold off;

%     Save figs
    if svoption
        savefig(fig, fullfile(svpath, [svfile, '.fig']));
        close (fig); 
    end