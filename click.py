class ResultSlide(BoxLayout):
    rotation_y = NumericProperty(0)  # Needed for animation
    raw_image = StringProperty("")
    processed_image = StringProperty("")
    diagnosis = StringProperty("")
    confidence = NumericProperty(0)

    def __init__(self, result, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Store details.
        self.raw_image = result.get('raw_image', "")
        self.processed_image = result.get('processed_image', "")
        self.diagnosis = result['diagnosis']
        self.confidence = float(result.get('confidence', 0))
        
        self.display_image_view()

    def display_image_view(self, instance=None):  # Accept optional argument
        self.clear_widgets()
        
        # Create a horizontal layout to show images side by side.
        images_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.7))
        
        # Processed image (background removed) on the left.
        proc_img = Image(source=self.processed_image, allow_stretch=True, size_hint=(0.5, 1))
        images_layout.add_widget(proc_img)
        
        # Raw captured image on the right.
        raw_img = Image(source=self.raw_image, allow_stretch=True, size_hint=(0.5, 1))
        images_layout.add_widget(raw_img)
        
        self.add_widget(images_layout)
        
        # Display diagnosis and confidence.
        diag_text = f"Diagnosis: {self.diagnosis}"
        if self.confidence:
            diag_text += f" ({self.confidence:.1f}%)"
        diag_label = Label(text=diag_text, size_hint=(1, 0.1))
        self.add_widget(diag_label)
        
        # 'More Info' button.
        more_info_button = Button(text="More Info", size_hint=(0.2, 0.1))
        more_info_button.bind(on_release=self.flip_view)
        self.add_widget(more_info_button)
    
    def flip_view(self, instance):
        anim = Animation(rotation_y=90, duration=0.3) + Animation(rotation_y=0, duration=0.3)
        anim.start(self)
        self.clear_widgets()
        
        # (Your recommendations code here; unchanged)
        if self.diagnosis == "Bacterial Blight":
            eng_msg = ("Bacterial Blight detected.\n"
                       "- Remove and destroy severely infected plants.\n"
                       "- Apply a copper-based bactericide as recommended.\n"
                       "- Maintain strict field hygiene.")
            fil_msg = ("Nadiskubre ang Bacterial Blight.\n"
                       "- Alisin at sirain ang labis na apektadong halaman.\n"
                       "- Gumamit ng copper-based bactericide.\n"
                       "- Panatilihin ang kalinisan ng taniman.")
        elif self.diagnosis in ["Blast", "Leaf Blast"]:
            eng_msg = ("Leaf Blast detected.\n"
                       "- Apply an effective fungicide.\n"
                       "- Adjust fertilizer use to avoid excessive growth.\n"
                       "- Improve plant spacing to enhance air circulation.\n"
                       "- Consult local agricultural services for guidance.")
            fil_msg = ("Nadiskubre ang Leaf Blast.\n"
                       "- Gamitin ng fungicide.\n"
                       "- Baguhin ang pataba para hindi magsobra ang paglaki.\n"
                       "- Ayusin ang pagitan ng mga halaman para sa mas maayos na sirkulasyon ng hangin.\n"
                       "- Kumonsulta sa lokal na agricultural service para sa payo.")
        elif self.diagnosis == "Brown Spot":
            eng_msg = ("Brown Spot detected.\n"
                       "- Use an appropriate fungicide.\n"
                       "- Avoid over-fertilization.\n"
                       "- Remove dead plant material to reduce spread.\n"
                       "- Follow good cultural practices.")
            fil_msg = ("Nadiskubre ang Brown Spot.\n"
                       "- Gamitin ang tamang fungicide.\n"
                       "- Iwasan ang paglalagay ng sobrang pataba.\n"
                       "- Alisin ang mga patay na bahagi ng halaman.\n"
                       "- Panatilihin ang tamang pamamahala ng taniman.")
        elif self.diagnosis == "Healthy":
            eng_msg = ("Your rice leaf appears healthy.\n"
                       "- Keep up your current cultivation practices and monitor regularly.")
            fil_msg = ("Malusog ang iyong dahon ng palay.\n"
                       "- Ipagpatuloy ang kasalukuyang pamamaraan at regular na i-monitor ang taniman.")
        elif self.diagnosis == "Not Rice":
            eng_msg = ("The image does not seem to be of a rice leaf.\n"
                       "- Please scan a proper rice leaf for an accurate diagnosis.")
            fil_msg = ("Ang larawan ay hindi mukhang dahon ng palay.\n"
                       "- Mangyaring mag-scan ng wastong dahon ng palay para sa maayos na diagnosis.")
        else:
            eng_msg = "No specific recommendations available."
            fil_msg = ""
        
        if fil_msg:
            fil_msg = f"[i]{fil_msg}[/i]"
        combined_text = f"Recommendations:\n{eng_msg}\n\n{fil_msg}"
        
        rec_label = Label(text=combined_text, markup=True, halign="center", size_hint=(1, 0.6))
        self.add_widget(rec_label)
        
        back_button = Button(text="See Image", size_hint=(0.3, 0.1))
        back_button.bind(on_release=self.display_image_view)
        self.add_widget(back_button)
