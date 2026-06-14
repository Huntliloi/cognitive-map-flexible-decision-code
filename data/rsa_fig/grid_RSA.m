%% LOAD DATA
% load the model with the periodicity you want to test
clear all;clc;close all;
roi = {'ECr'};
model.m4 = csvread(['E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\model\RDM_hudu_SR3Model-4fold.csv']);
model.m5 = csvread(['E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\model\RDM_hudu_SR3Model-5fold.csv']);
model.m6 = csvread(['E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\model\RDM_hudu_SR3Model-6fold.csv']);
model.m7 = csvread(['E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\model\RDM_hudu_SR3Model-7fold.csv']);
% load participation data
Path=['E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\rdm_pre_roi\'];
File = dir(fullfile(Path,'RDM_*.csv'));
Len=length(File);

for s=1:Len
    filename=strcat(Path,File(s).name);
    fm=csvread(filename,1,0);
    neuro_du.ECr(s,:,:)=squeeze(fm); 
end

clear File filename fm Len Path s

%% start compute 
current_model = {'m4','m5','m6','m7'};
fieldNames = fieldnames(neuro_du);
for i=1:length(current_model)
    for subj = 1:size(neuro_du.(fieldNames{1}),1)
        for r =1:length(roi)
           dsms = [cosmo_squareform(squeeze(neuro_du.(roi{r})(subj,:,:)))', cosmo_squareform(eval(['model.',current_model{i}]))'];
           cc = cosmo_corr(dsms);
           model_results.(current_model{i})(subj,r) = cc(1,2);
        end
    end
end

% roi_results.ECr = [model_results.m4,model_results.m5,model_results.m6,model_results.m7];
roi_results.ECr = [post.m4,post.m5,post.m6,post.m7];
%% Plot
for r =1:1
    figure('Color', 'white'); % 设置图形窗口背景为白色
    [h, p, ci, stats] = ttest(roi_results.(roi{r}), 0, 'Tail', 'both');
    [h,p0(:,1)] = ttest2(roi_results.(roi{r})(:,3), roi_results.(roi{r})(:,1),'Tail', 'both');
    [h,p0(:,2)] = ttest2(roi_results.(roi{r})(:,3), roi_results.(roi{r})(:,2),'Tail', 'both');
    [h,p0(:,3)] = ttest2(roi_results.(roi{r})(:,3), roi_results.(roi{r})(:,4),'Tail', 'both');
    %   P值统计校正
    corrected_p = round(mafdr([p(3),p0], 'BHFDR', true),2);
    P_model = corrected_p(1);
    p1 = [corrected_p(2)];
    p2 = [0,corrected_p(3),corrected_p(4)];
    means = mean(roi_results.(roi{r}));
    errors = std(roi_results.(roi{r})) ./ sqrt(size(roi_results.(roi{r}), 1));
    All.(roi{r}) = [(4:7)',means',errors',p'];
    bar(means, 'FaceColor', [0.7, 0.7, 0.7], 'EdgeColor', 'k')
    hold on;
    errorbar(1:4, means, errors, 'k', 'linestyle', 'none','LineWidth', 1.5); % 'k' 表示误差棒为黑色
    % 设置坐标轴标签
    xlabel('-fold', 'FontWeight', 'bold', 'FontSize', 12);
    ylabel('correlation', 'FontWeight', 'bold', 'FontSize', 12);
    % 设置刻度和字体加粗
    set(gca, 'FontSize', 24, 'FontWeight', 'bold');
    % 设置刻度线方向朝外
    set(gca, 'TickDir', 'out');
    % 去除边框并设置背景为白色
    set(gca, 'box', 'off', 'Color', 'white');
    % 设置y轴范围
    ylim([-0.1 0.2]);
    % 设置x轴刻度
    set(gca, 'XTick', 1:4);
    xticklabels({'4-fold', '5-fold', '6-fold','7-fold'});
    ax = gca; % 获取当前轴
    ax.XTickLabelRotation = 20; % 将 x 轴标签倾斜 20 度
%     ax.XAxis.TickLabelAlignment = 'center'; % 仅限于较新版本的 MATLAB
    [val,index] =  max(means);
    y = val+errors(index);
    % 本身线
    for i=1
        sigline(i+2,y+0.01,P_model(i));
    end
    for i=1:2:2
        sigline([i,i+2],y+i*0.005+0.02,p1(i));
    end
    for i=2:1:3
        sigline([i,i+1],y+i*0.006+0.03,p2(i));
    end
%     saveas(gcf, ['E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\roi{r}post,'.fig']);
end


figure('Color', 'white'); % 设置图形窗口背景为白色
hold on;
% 盒须图
% load('E:\3、论文撰写\【表征学习】\数据及代码整理\Fig45_RSA\grid-RSA\ECr_ROI.mat')
A = [pre.m6,post.m6];
[h,p] = ttest2(A(:,2), A(:,1),'Tail', 'both')
boxplot(A, 'Widths', 0.5, 'Colors', 'k', 'Positions', 1:2);
set(gca, 'TickDir', 'out');
set(gca, 'FontSize', 24, 'FontWeight', 'bold');
set(gca, 'box', 'off', 'Color', 'white');
xticklabels({'pre6-fold','post6-fold'});
colors = lines(24);
for i = 1:2
    scatter(repmat(i,24,1), A(:,i),100, colors, 'filled', 'MarkerFaceAlpha', 0.3);
end

% 绘制从 Group 1 到 Group 2 的直线
for i = 1:24
    plot([1 2], [A(i, 1) A(i, 2)], 'Color', colors(i, :), 'LineWidth', 1.5);  % 连接点的线条
end
sigline([1,2],0.4+0.03,p);

