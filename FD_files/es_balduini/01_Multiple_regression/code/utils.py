import statsmodels.api as sm
import pandas as pd
from itertools import combinations
import plotly.graph_objects as go
import numpy as np

def extract_regression_summary(results):
    """
    Extracts key regression statistics from a statsmodels results object 
    and returns a summary DataFrame.
    
    Parameters:
        results: statsmodels regression results object.
    
    Returns:
        pd.DataFrame: A DataFrame with coefficients, standard errors, t-values,
                      p-values, and confidence intervals.
    """
    coefficients = results.params
    std_err = results.bse
    t_values = results.tvalues
    p_values = results.pvalues
    conf_int = results.conf_int()
    
    # Create the summary DataFrame
    summary_df = pd.DataFrame({
        "coef": coefficients,
        "std err": std_err,
        "t": t_values,
        "P>|t|": p_values,
        "0.025": conf_int[0],
        "0.975": conf_int[1]
    })
    
    return summary_df

def forward_selection(data, response):
    """
    Perform forward selection to find the best features based on AIC.

    Parameters:
    - data: pandas DataFrame containing predictor variables.
    - response: pandas Series or array-like target variable.

    Returns:
    - best_features: List of selected features in order of inclusion.
    """
    initial_features = []
    remaining_features = list(data.columns)
    best_features = []
    current_aic = float('inf')
    
    while remaining_features:
        scores = []
        for feature in remaining_features:
            features_to_test = initial_features + [feature]
            X = sm.add_constant(data[features_to_test])
            model = sm.OLS(response, X).fit()
            scores.append((model.aic, feature))
        
        # Find the best feature based on the lowest AIC
        scores.sort()
        best_score, best_feature = scores[0]
        
        # Check if adding the feature improves the AIC
        if best_score < current_aic:
            current_aic = best_score
            best_features.append(best_feature)
            initial_features.append(best_feature)
            remaining_features.remove(best_feature)
            print(f"Adding feature: {best_feature} with AIC: {best_score}")
        else:
            # Stop if no improvement in AIC
            break
    
    return best_features

def backward_elimination(data, response, significance_level=0.05):
    features = list(data.columns)
    while len(features) > 0:
        X = sm.add_constant(data[features])
        model = sm.OLS(response, X).fit()
        p_values = model.pvalues.iloc[1:]  # Exclude intercept
        max_p_value = p_values.max()
        
        if max_p_value > significance_level:
            excluded_feature = p_values.idxmax()
            features.remove(excluded_feature)
            print(f"Removing feature: {excluded_feature} with p-value: {max_p_value}")
        else:
            break
    
    return features


def stepwise_selection(data, response, significance_level_in=0.05, significance_level_out=0.05):
    """
    Perform stepwise feature selection based on AIC for forward selection
    and p-values for backward elimination.
    
    Parameters:
    - data: DataFrame containing predictors.
    - response: Series containing the target variable.
    - significance_level_in: Significance level for adding features.
    - significance_level_out: Significance level for removing features.
    
    Returns:
    - List of selected features.
    """
    selected_features = []
    remaining_features = list(data.columns)
    last_aic = float('inf')
    
    while True:
        # Forward Step: Try adding features
        forward_candidates = []
        for feature in remaining_features:
            features_to_test = selected_features + [feature]
            X = sm.add_constant(data[features_to_test])
            model = sm.OLS(response, X).fit()
            forward_candidates.append((model.aic, feature))
        
        forward_candidates.sort()
        if forward_candidates:
            best_aic, best_feature = forward_candidates[0]
            if best_aic < last_aic:  # Add feature if it improves AIC
                selected_features.append(best_feature)
                remaining_features.remove(best_feature)
                last_aic = best_aic
                print(f"Adding feature: {best_feature} with AIC: {best_aic}")
            else:
                break  # Stop if no improvement
        
        # Backward Step: Try removing features
        backward_candidates = []
        X = sm.add_constant(data[selected_features])
        model = sm.OLS(response, X).fit()
        p_values = model.pvalues.iloc[1:]  # Exclude intercept
        
        for feature, p_value in p_values.items():
            if p_value > significance_level_out:
                backward_candidates.append((p_value, feature))
        
        if backward_candidates:
            backward_candidates.sort(reverse=True)  # Sort by p-value descending
            worst_p_value, worst_feature = backward_candidates[0]
            selected_features.remove(worst_feature)
            remaining_features.append(worst_feature)
            print(f"Removing feature: {worst_feature} with p-value: {worst_p_value}")
        
        # Break condition: No forward or backward changes
        if not forward_candidates and not backward_candidates:
            break
    
    return selected_features

def plot_3d_hyperplane(model, X, Y, predictor1, predictor2, title='3D Regression Hyperplane'):
    """
    Visualizes a 3D regression hyperplane with actual data points.

    Parameters:
    - model: The statsmodels fitted OLS model.
    - X: DataFrame containing predictor variables.
    - Y: Series or array of actual target values.
    - predictor1: The name of the first predictor variable (x-axis).
    - predictor2: The name of the second predictor variable (y-axis).
    - title: Title of the 3D plot (default is '3D Regression Hyperplane').
    
    Returns:
    - fig: The Plotly Figure object for further customization or saving.
    """
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    # Ensure predictors exist in the DataFrame
    for predictor in [predictor1, predictor2]:
        if predictor not in X.columns:
            raise ValueError(f"Predictor '{predictor}' not found in the input DataFrame.")

    # Generate grid for the surface plot
    range1 = np.linspace(X[predictor1].min(), X[predictor1].max(), 50)
    range2 = np.linspace(X[predictor2].min(), X[predictor2].max(), 50)
    grid1, grid2 = np.meshgrid(range1, range2)

    # Prepare a DataFrame for model prediction
    X_grid = pd.DataFrame({
        'const': 1,
        predictor1: grid1.ravel(),
        predictor2: grid2.ravel()
    })

    # Ensure all other variables in the model are included, set to their means
    for col in model.params.index:
        if col not in X_grid.columns:
            X_grid[col] = X[col].mean()

    # Predict values and reshape for surface plotting
    predicted_values = model.predict(X_grid).values.reshape(grid1.shape)

    # Create 3D plot
    fig = go.Figure()

    # Add actual data points
    fig.add_trace(go.Scatter3d(
        x=X[predictor1],
        y=X[predictor2],
        z=Y,
        mode='markers',
        marker=dict(size=5, color='blue', opacity=0.7),
        name='Actual Data',
        customdata=predicted_values.ravel(),
        hovertemplate=(
            f"<b>{predictor1}:</b> %{{x:.2f}}<br>"
            f"<b>{predictor2}:</b> %{{y:.2f}}<br>"
            f"<b>Y (Actual):</b> %{{z:.2f}}<br>"
            f"<b>Ŷ (Predicted):</b> %{{customdata:.2f}}<extra></extra>"
        )
    ))

    # Add regression hyperplane
    fig.add_trace(go.Surface(
        x=range1,
        y=range2,
        z=predicted_values,
        colorscale='Viridis',
        opacity=0.7,
        name='Regression Plane'
    ))

    # Customize layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=predictor1,
            yaxis_title=predictor2,
            zaxis_title='Target',
            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
            zaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
        ),
        margin=dict(l=20, r=20, b=20, t=40),
        width=900,
        height=700
    )
    return fig