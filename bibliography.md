Bibliography
-----------------------------
  
Here is the complete list of the published papers connected to the lessons deposited in PLUMED-TUTORIALS:

{% assign sorted_less = site.data.lessons | sort: "id" | reverse %}

{% for item in sorted_less %}
  {% if item.reference != 'unpublished' and item.reference != 'submitted' and item.reference != 'DOI not found' %}
   [[ID:{{ item.id }}]({{ item.path }})] [{{ item.reference }}]({{ item.ref_url }})
 {% endif %}
{% endfor %}

Further reading
------------------------------------
Here you can find a list of additional papers containing practical PLUMED tutorials:

* [Bussi, G. and Tribello, G. A. (2019) Analyzing and biasing simulations with PLUMED](https://arxiv.org/abs/1812.08213)

* [Barducci A., Pfaendtner J., Bonomi M. (2015) Tackling Sampling Challenges in Biomolecular Simulations. In: Kukol A. (eds) Molecular Modeling of Proteins. Methods in Molecular Biology (Methods and Protocols), vol 1215. Humana Press, New York, NY](https://link.springer.com/protocol/10.1007/978-1-4939-1465-4_8)

* [Bussi, G. and Branduardi, D. (2015). Free‐Energy Calculations with Metadynamics: Theory and Practice. In Reviews in Computational Chemistry Volume 28 (eds A. L. Parrill and K. B. Lipkowitz)](https://onlinelibrary.wiley.com/doi/10.1002/9781118889886.ch1)
