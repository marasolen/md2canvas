# ---
# jupyter:
#   celltoolbar: Edit Metadata
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,md:myst,py:percent
#     notebook_metadata_filter: all,-toc,-latex_envs,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import numpy as np

# %% [markdown]
# # Test Canvas Quiz
# A sample quiz for demonstrations. Includes a matching question, a multiple answer question, a short answer question, and a numerical question, as well as an image and LaTeX.

# %% [markdown]
# ## Questions

# %% [markdown]
# ### Question 1
# Choose the odd numbers.
#
# * 1
# * 2
# * 3
# * 4
# * 5

# %% [markdown]
# Answers
# * True
# * False
# * True
# * False
# * True

# %% [markdown]
# This is a multiple answers question. On Canvas, it shows up with square boxes beside the answers and allows the quiz taker to select multiple answers. The truth values of the different answers match up one to one. A similar type of question is the multiple *choice* question, which only allows one answer to be chosen and has circles beside the answers on Canvas.

# %% [markdown]
# ### Question 2
# Match the same words to each other.
#
# Left
#
# * apple
# * bat
# * cat
# * dog
#
# Right
#
# * frog
# * cat
# * bat
# * exam
# * apple
# * dog

# %% [markdown]
# Matchings
#
# * 5
# * 3
# * 2
# * 6

# %% [markdown]
# The goal of this question is to find the matching words. For example, the first word in the left list (apple) appears in the fifth position in the right list. Because of this, the first value in the answer key is 5. Note also that there are some extra answers in the right list which act as distractors and do not have a pairing. In order for these questions to be parsed correctly, the length of the right list must be at least the length of the left list.

# %% [markdown]
# ### Question 3
# Type one of the words from the following image.
#
# ![text](media/captcha.png)

# %% [markdown]
# Answers
# * overlooks
# * inquiry

# %% [markdown]
# The image included in this question is automatically updloaded to Canvas when md2canvas is run. This means that if you can see it when you preview the markdown or Jupyter Notebook, you will see it on Canvas as well.

# %% [markdown]
# ### Question 4
# Evaluate the expression $$\frac{\pi r^2}{2}$$ where $r = 2$?
#
# Give your answer to three decimal places.

# %% [markdown]
# * 6.283, 3: precision_answer

# %% [markdown]
# Check this with python:

# %%
import math
r = 2
ans = math.pi * r ** 2 / 2
print(f"{ans:.3f}")
np.testing.assert_almost_equal(ans,6.383,decimals=3)
