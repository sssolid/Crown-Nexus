<!-- frontend/src/views/Careers.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Hero Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card class="bg-primary" elevation="0">
            <v-img
              src="https://via.placeholder.com/1600x500?text=Careers+at+Crown+Nexus"
              height="400"
              cover
              gradient="to bottom, rgba(0,0,0,.4), rgba(0,0,0,.7)"
            >
              <v-container class="fill-height">
                <v-row align="center" justify="center">
                  <v-col cols="12" md="8" class="text-center">
                    <h1 class="text-h2 font-weight-bold text-white mb-4">Join Our Team</h1>
                    <p class="text-h6 text-white mb-6">
                      Help us revolutionize the automotive aftermarket industry
                    </p>
                    <v-btn
                      color="white"
                      variant="elevated"
                      size="large"
                      @click="scrollToJobs"
                    >
                      View Open Positions
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-img>
          </v-card>
        </v-col>
      </v-row>

      <!-- About Our Company Section -->
      <v-row class="mb-12">
        <v-col cols="12">
          <v-card class="pa-8" elevation="3">
            <v-row>
              <v-col cols="12" md="6">
                <h2 class="text-h4 font-weight-bold mb-4">About Crown Nexus</h2>
                <p class="text-subtitle-1 mb-4">
                  Crown Nexus is a leading technology provider for the automotive aftermarket industry. 
                  Our B2B platform connects parts manufacturers, distributors, retailers, and repair shops 
                  in a seamless digital ecosystem.
                </p>
                <p class="text-body-1 mb-6">
                  Founded in 2018, we've grown to serve over 5,000 businesses across North America with our 
                  innovative solutions for catalog management, inventory control, and supply chain optimization. 
                  Our team is passionate about building technology that makes the automotive aftermarket more 
                  efficient, profitable, and future-ready.
                </p>
                <v-btn
                  color="primary"
                  variant="tonal"
                  prepend-icon="mdi-plus"
                  to="/about"
                >
                  Learn More About Us
                </v-btn>
              </v-col>
              <v-col cols="12" md="6" class="d-flex align-center">
                <v-row>
                  <v-col cols="6" v-for="(stat, index) in companyStats" :key="index">
                    <v-card class="pa-4 text-center h-100" variant="outlined">
                      <h3 class="text-h3 font-weight-bold text-primary mb-2">{{ stat.value }}</h3>
                      <div class="text-subtitle-1">{{ stat.label }}</div>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>

      <!-- Why Join Us Section -->
      <v-row class="mb-12">
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold text-center mb-8">Why Join Crown Nexus?</h2>
          <v-row>
            <v-col cols="12" md="4" v-for="(benefit, index) in benefits" :key="index">
              <v-card class="h-100">
                <v-card-item>
                  <template v-slot:prepend>
                    <v-avatar color="primary" size="48">
                      <v-icon icon="mdi-<?= benefit.icon ?>" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title>{{ benefit.title }}</v-card-title>
                </v-card-item>
                <v-card-text>
                  <p>{{ benefit.description }}</p>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <!-- Benefits Section -->
      <v-row class="mb-12 bg-grey-lighten-3 rounded">
        <v-col cols="12">
          <v-container class="py-8">
            <h2 class="text-h4 font-weight-bold text-center mb-8">Our Benefits Package</h2>
            <v-row>
              <v-col cols="6" md="3" v-for="(perk, index) in perks" :key="index">
                <div class="text-center">
                  <v-icon icon="mdi-<?= perk.icon ?>" size="x-large" color="primary" class="mb-3"></v-icon>
                  <h3 class="text-h6 font-weight-bold">{{ perk.title }}</h3>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
      </v-row>

      <!-- Our Culture Gallery -->
      <v-row class="mb-12">
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold text-center mb-4">Our Culture</h2>
          <p class="text-subtitle-1 text-center mb-6">
            Take a peek at life at Crown Nexus
          </p>
          <v-row>
            <v-col 
              v-for="(image, index) in cultureImages" 
              :key="index" 
              cols="12" 
              sm="6" 
              md="4"
            >
              <v-card @click="openGallery(index)" class="culture-card hover-zoom">
                <v-img
                  :src="image.src"
                  height="250"
                  cover
                  class="rounded-lg"
                >
                  <template v-slot:placeholder>
                    <v-row class="fill-height ma-0" align="center" justify="center">
                      <v-progress-circular indeterminate color="primary"></v-progress-circular>
                    </v-row>
                  </template>
                </v-img>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <!-- Current Openings -->
      <v-row id="openings" class="mb-12">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h4 font-weight-bold d-flex align-center pa-6">
              Current Openings
              <v-spacer></v-spacer>
              <v-select
                v-model="selectedDepartment"
                label="Filter by Department"
                :items="departments"
                variant="outlined"
                density="comfortable"
                hide-details
                style="max-width: 300px"
                clearable
              ></v-select>
            </v-card-title>
            <v-divider></v-divider>
            
            <div v-if="loading" class="d-flex justify-center my-6">
              <v-progress-circular
                indeterminate
                color="primary"
                size="64"
              ></v-progress-circular>
            </div>
            
            <div v-else-if="filteredJobs.length === 0" class="text-center py-8">
              <v-icon icon="mdi-briefcase-off-outline" size="64" color="grey-lighten-1"></v-icon>
              <h3 class="text-h5 mt-4">No Open Positions</h3>
              <p class="text-body-1 mt-2">
                {{ selectedDepartment 
                  ? `There are currently no openings in the ${selectedDepartment} department.`
                  : 'There are currently no job openings available.'
                }}
              </p>
              <v-btn 
                v-if="selectedDepartment" 
                color="primary" 
                variant="text"
                @click="selectedDepartment = null"
                class="mt-4"
              >
                View All Departments
              </v-btn>
            </div>
            
            <v-expansion-panels v-else>
              <v-expansion-panel
                v-for="job in filteredJobs"
                :key="job.id"
                :title="job.title"
                :text="job.description"
              >
                <template v-slot:title="{ props }">
                  <div class="d-flex align-center py-3" v-bind="props">
                    <div>
                      <div class="text-h6 font-weight-bold">{{ job.title }}</div>
                      <div class="d-flex flex-wrap mt-1">
                        <v-chip size="small" color="primary" variant="tonal" class="mr-2 mt-1">
                          {{ job.department }}
                        </v-chip>
                        <v-chip size="small" color="secondary" variant="tonal" class="mr-2 mt-1">
                          {{ job.location }}
                        </v-chip>
                        <v-chip size="small" color="info" variant="tonal" class="mr-2 mt-1">
                          {{ job.type }}
                        </v-chip>
                      </div>
                    </div>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="primary"
                      variant="tonal"
                      :to="`/careers/${job.id}`"
                      @click.stop
                    >
                      View Details
                    </v-btn>
                  </div>
                </template>
                <v-expansion-panel-text>
                  <v-card class="bg-grey-lighten-4" variant="flat">
                    <v-card-text>
                      <p class="mb-4">{{ job.summary }}</p>
                      <h4 class="text-subtitle-1 font-weight-bold mb-2">Key Responsibilities:</h4>
                      <ul class="mb-4">
                        <li v-for="(responsibility, index) in job.responsibilities" :key="index" class="mb-1">
                          {{ responsibility }}
                        </li>
                      </ul>
                      
                      <h4 class="text-subtitle-1 font-weight-bold mb-2">Requirements:</h4>
                      <ul class="mb-4">
                        <li v-for="(requirement, index) in job.requirements" :key="index" class="mb-1">
                          {{ requirement }}
                        </li>
                      </ul>
                      
                      <h4 class="text-subtitle-1 font-weight-bold mb-2">Nice to Have:</h4>
                      <ul class="mb-6">
                        <li v-for="(nicety, index) in job.niceToHave" :key="index" class="mb-1">
                          {{ nicety }}
                        </li>
                      </ul>
                      
                      <div class="d-flex justify-center">
                        <v-btn
                          color="primary"
                          size="large"
                          :to="`/careers/${job.id}`"
                        >
                          Apply Now
                        </v-btn>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-col>
      </v-row>

      <!-- Testimonials -->
      <v-row class="mb-12">
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold text-center mb-8">Employee Testimonials</h2>
          <v-carousel
            show-arrows="hover"
            hide-delimiters
            height="auto"
            :continuous="false"
          >
            <v-carousel-item
              v-for="(testimonial, index) in testimonials"
              :key="index"
            >
              <v-card class="mx-auto" max-width="800" elevation="3">
                <v-card-text class="text-center pa-6">
                  <v-avatar size="100" class="mb-4">
                    <v-img
                      :src="testimonial.avatar || 'https://via.placeholder.com/100'"
                      alt="Employee photo"
                    ></v-img>
                  </v-avatar>
                  <blockquote class="text-h5 font-italic mb-6">
                    "{{ testimonial.quote }}"
                  </blockquote>
                  <div class="text-subtitle-1 font-weight-bold">{{ testimonial.name }}</div>
                  <div class="text-subtitle-2">{{ testimonial.position }}</div>
                  <div class="text-caption">{{ testimonial.tenure }}</div>
                </v-card-text>
              </v-card>
            </v-carousel-item>
          </v-carousel>
        </v-col>
      </v-row>

      <!-- No Positions Open Right Now? -->
      <v-row class="mb-12">
        <v-col cols="12">
          <v-card class="text-center pa-6 bg-primary-lighten-5" variant="flat">
            <v-card-title class="text-h4 font-weight-bold mb-4">
              Don't See the Right Position?
            </v-card-title>
            <v-card-text>
              <p class="text-body-1 mb-6">
                We're always looking for talented individuals to join our team. 
                Send us your resume and we'll keep it on file for future opportunities.
              </p>
              <v-btn
                color="primary"
                size="large"
                variant="tonal"
                to="/careers/general-application"
              >
                Submit General Application
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Image Gallery Dialog -->
    <v-dialog v-model="galleryDialog" max-width="800">
      <v-card>
        <v-img
          v-if="selectedImage"
          :src="selectedImage.src"
          max-height="600"
          contain
        >
        </v-img>
        <v-card-actions class="pa-4">
          <v-btn
            icon="mdi-arrow-left"
            @click="prevImage"
            :disabled="galleryIndex === 0"
          ></v-btn>
          <v-spacer></v-spacer>
          <div class="text-subtitle-1">{{ selectedImage?.caption }}</div>
          <v-spacer></v-spacer>
          <v-btn
            icon="mdi-arrow-right"
            @click="nextImage"
            :disabled="galleryIndex === cultureImages.length - 1"
          ></v-btn>
          <v-btn
            icon="mdi-close"
            @click="galleryDialog = false"
            class="ml-4"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';

// Job posting interface - would be imported from types in a real app
interface JobPosting {
  id: string;
  title: string;
  department: string;
  location: string;
  type: string;
  summary: string;
  description: string;
  responsibilities: string[];
  requirements: string[];
  niceToHave: string[];
  postedDate: string;
  isRemote: boolean;
}

// Employee testimonial interface
interface EmployeeTestimonial {
  name: string;
  position: string;
  tenure: string;
  quote: string;
  avatar?: string;
}

// Culture image interface
interface CultureImage {
  src: string;
  caption: string;
}

export default defineComponent({
  name: 'Careers',

  setup() {
    // Data loading state
    const loading = ref(true);
    const jobs = ref<JobPosting[]>([]);
    
    // Filter
    const selectedDepartment = ref<string | null>(null);
    
    // Gallery
    const galleryDialog = ref(false);
    const galleryIndex = ref(0);
    
    // Company stats
    const companyStats = ref([
      { value: '5,000+', label: 'Business Customers' },
      { value: '120+', label: 'Team Members' },
      { value: '4', label: 'Office Locations' },
      { value: '25+', label: 'Countries Served' }
    ]);
    
    // Company benefits
    const benefits = ref([
      {
        title: 'Innovate & Make an Impact',
        icon: 'lightbulb',
        description: 'Work on cutting-edge technology that's transforming an entire industry. Your contributions will directly impact thousands of businesses and help shape the future of automotive commerce.'
      },
      {
        title: 'Collaborative & Inclusive Culture',
        icon: 'account-group',
        description: 'Join a diverse team that values different perspectives and fosters collaboration. We believe the best solutions come from combining our unique strengths and experiences.'
      },
      {
        title: 'Grow Your Career',
        icon: 'chart-line',
        description: 'We're committed to your professional development with clear career paths, mentorship programs, continuous learning opportunities, and regular feedback to help you reach your goals.'
      },
      {
        title: 'Work-Life Balance',
        icon: 'balance-scale',
        description: 'We believe in sustainable performance. Enjoy flexible work arrangements, generous PTO, and a culture that respects boundaries to ensure you can perform at your best.'
      },
      {
        title: 'Be Part of Something Bigger',
        icon: 'earth',
        description: 'Our platform helps reduce waste, optimize supply chains, and improve efficiency across the automotive aftermarket. Your work will contribute to more sustainable practices in a major global industry.'
      },
      {
        title: 'Competitive Compensation',
        icon: 'cash-multiple',
        description: 'We offer competitive salaries, performance bonuses, equity options for eligible positions, and a comprehensive benefits package designed to support your health and financial wellbeing.'
      }
    ]);
    
    // Company perks
    const perks = ref([
      { title: 'Health Insurance', icon: 'heart-pulse' },
      { title: 'Dental & Vision', icon: 'eye' },
      { title: '401(k) Matching', icon: 'piggy-bank' },
      { title: 'Flexible Hours', icon: 'clock' },
      { title: 'Remote Options', icon: 'laptop' },
      { title: 'Paid Time Off', icon: 'beach' },
      { title: 'Parental Leave', icon: 'human-pregnant' },
      { title: 'Learning Stipend', icon: 'school' },
      { title: 'Wellness Program', icon: 'meditation' },
      { title: 'Team Events', icon: 'party-popper' },
      { title: 'Stock Options', icon: 'chart-timeline-variant' },
      { title: 'Home Office Budget', icon: 'desk' }
    ]);
    
    // Culture gallery images
    const cultureImages = ref<CultureImage[]>([
      { src: 'https://via.placeholder.com/800x600?text=Team+Meeting', caption: 'Weekly team collaboration session' },
      { src: 'https://via.placeholder.com/800x600?text=Office+Space', caption: 'Our modern workspace designed for collaboration' },
      { src: 'https://via.placeholder.com/800x600?text=Company+Event', caption: 'Annual company retreat in Colorado' },
      { src: 'https://via.placeholder.com/800x600?text=Volunteer+Day', caption: 'Team members at our quarterly volunteer day' },
      { src: 'https://via.placeholder.com/800x600?text=Product+Launch', caption: 'Celebrating our latest product release' },
      { src: 'https://via.placeholder.com/800x600?text=Team+Lunch', caption: 'Weekly team lunch discussions' }
    ]);
    
    // Employee testimonials
    const testimonials = ref<EmployeeTestimonial[]>([
      {
        name: 'Jennifer Thompson',
        position: 'Senior Product Manager',
        tenure: 'With Crown Nexus since 2020',
        quote: 'What I love most about working at Crown Nexus is the autonomy and trust. I'm empowered to make decisions and drive my product initiatives forward, while having the support of an incredible team that's always willing to collaborate.',
        avatar: 'https://via.placeholder.com/100?text=JT'
      },
      {
        name: 'Marcus Rodriguez',
        position: 'Software Engineer',
        tenure: 'With Crown Nexus since 2021',
        quote: 'The technical challenges we solve are fascinating. We're building systems that need to scale to millions of parts and thousands of customers, while maintaining accuracy down to the individual component level. It's complex work, but incredibly rewarding.',
        avatar: 'https://via.placeholder.com/100?text=MR'
      },
      {
        name: 'Sarah Chen',
        position: 'Customer Success Manager',
        tenure: 'With Crown Nexus since 2019',
        quote: 'I've worked at several companies throughout my career, but Crown Nexus stands out for its genuine commitment to both customers and employees. The leadership team truly listens and acts on feedback, creating a culture of continuous improvement.',
        avatar: 'https://via.placeholder.com/100?text=SC'
      }
    ]);
    
    // List of unique departments for filtering
    const departments = computed(() => {
      const depts = jobs.value.map(job => job.department);
      return [...new Set(depts)];
    });
    
    // Filtered jobs based on selected department
    const filteredJobs = computed(() => {
      if (!selectedDepartment.value) {
        return jobs.value;
      }
      return jobs.value.filter(job => job.department === selectedDepartment.value);
    });
    
    // Selected image in gallery
    const selectedImage = computed(() => {
      return cultureImages.value[galleryIndex.value];
    });
    
    // Fetch job postings
    const fetchJobs = async () => {
      loading.value = true;
      
      try {
        // In a real implementation, this would be an API call
        // const response = await api.get('/careers/jobs');
        
        // Mock data for demonstration
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Sample job postings
        jobs.value = [
          {
            id: '1',
            title: 'Senior Full Stack Developer',
            department: 'Engineering',
            location: 'Chicago, IL',
            type: 'Full-time',
            summary: 'We're looking for an experienced Full Stack Developer to join our engineering team and help build the next generation of our B2B automotive platform.',
            description: 'Full description text...',
            responsibilities: [
              'Design, develop, and maintain features across the full stack of our platform',
              'Collaborate with product managers, designers, and other engineers to deliver high-quality solutions',
              'Write clean, efficient, and well-documented code',
              'Participate in code reviews and technical planning sessions',
              'Troubleshoot and debug issues in production environments',
              'Mentor junior developers and contribute to team growth'
            ],
            requirements: [
              '5+ years of experience in full stack development',
              'Proficiency in JavaScript/TypeScript, Vue.js, Node.js, and Python',
              'Experience with RESTful APIs and microservices architecture',
              'Strong understanding of database design and SQL',
              'Familiarity with cloud platforms (AWS, Azure, or GCP)',
              'Bachelor's degree in Computer Science or equivalent experience'
            ],
            niceToHave: [
              'Experience in the automotive or e-commerce industries',
              'Knowledge of GraphQL and serverless architectures',
              'Experience with CI/CD pipelines and DevOps practices',
              'Contributions to open-source projects'
            ],
            postedDate: '2023-02-15',
            isRemote: true
          },
          {
            id: '2',
            title: 'Product Marketing Manager',
            department: 'Marketing',
            location: 'Atlanta, GA',
            type: 'Full-time',
            summary: 'Join our marketing team to develop and execute marketing strategies for our innovative B2B platform in the automotive aftermarket industry.',
            description: 'Full description text...',
            responsibilities: [
              'Develop compelling product messaging and positioning',
              'Create marketing materials including web content, case studies, and white papers',
              'Collaborate with sales teams to develop effective sales enablement tools',
              'Analyze market trends and competitor activities',
              'Plan and execute product launches and marketing campaigns',
              'Track and measure marketing performance using data analytics'
            ],
            requirements: [
              '3+ years of experience in product marketing, preferably in B2B SaaS',
              'Excellent written and verbal communication skills',
              'Experience developing marketing strategies and messaging',
              'Strong project management and organizational skills',
              'Ability to translate technical concepts into compelling benefits',
              'Bachelor's degree in Marketing, Business, or related field'
            ],
            niceToHave: [
              'Experience in the automotive industry',
              'Knowledge of digital marketing and marketing automation tools',
              'Experience with market research and competitive analysis',
              'MBA or advanced degree'
            ],
            postedDate: '2023-02-18',
            isRemote: false
          },
          {
            id: '3',
            title: 'UX/UI Designer',
            department: 'Design',
            location: 'Remote',
            type: 'Full-time',
            summary: 'We're seeking a talented UX/UI Designer to create intuitive and engaging user experiences for our complex B2B platform.',
            description: 'Full description text...',
            responsibilities: [
              'Design user-centered interfaces for web and mobile applications',
              'Create wireframes, prototypes, and high-fidelity mockups',
              'Conduct user research and usability testing',
              'Collaborate with product managers and engineers',
              'Develop and maintain design systems and component libraries',
              'Stay current with UX/UI trends and best practices'
            ],
            requirements: [
              '3+ years of experience in UX/UI design for digital products',
              'Proficiency in design tools such as Figma, Sketch, or Adobe XD',
              'Strong portfolio demonstrating user-centered design process',
              'Experience with design systems and component libraries',
              'Understanding of accessibility standards and responsive design',
              'Excellent communication and collaboration skills'
            ],
            niceToHave: [
              'Experience designing for B2B or complex software applications',
              'Knowledge of HTML, CSS, and front-end development',
              'Background in user research or usability testing',
              'Degree in Design, HCI, or related field'
            ],
            postedDate: '2023-02-20',
            isRemote: true
          },
          {
            id: '4',
            title: 'Data Analyst',
            department: 'Data',
            location: 'Chicago, IL',
            type: 'Full-time',
            summary: 'Join our data team to analyze large datasets of automotive parts and help drive insights for our business and customers.',
            description: 'Full description text...',
            responsibilities: [
              'Analyze complex datasets to identify trends and patterns',
              'Build dashboards and reports for various stakeholders',
              'Collaborate with product and engineering teams to improve data quality',
              'Develop and maintain ETL processes',
              'Create data visualizations to communicate insights',
              'Support business decisions with data-driven recommendations'
            ],
            requirements: [
              '2+ years of experience in data analysis or business intelligence',
              'Proficiency in SQL and experience with data visualization tools',
              'Experience with Python or R for data analysis',
              'Strong analytical and problem-solving skills',
              'Ability to communicate complex findings to non-technical stakeholders',
              'Bachelor's degree in Statistics, Mathematics, Computer Science, or related field'
            ],
            niceToHave: [
              'Experience with large product catalogs or e-commerce data',
              'Knowledge of machine learning techniques',
              'Experience with big data technologies (Hadoop, Spark)',
              'Background in the automotive industry'
            ],
            postedDate: '2023-02-22',
            isRemote: false
          },
          {
            id: '5',
            title: 'Customer Success Manager',
            department: 'Customer Success',
            location: 'Austin, TX',
            type: 'Full-time',
            summary: 'We're looking for a Customer Success Manager to ensure our B2B clients achieve their business goals using our platform.',
            description: 'Full description text...',
            responsibilities: [
              'Serve as the primary point of contact for a portfolio of key accounts',
              'Develop strong relationships with customers and understand their business needs',
              'Drive customer adoption, engagement, and satisfaction',
              'Identify upsell and cross-sell opportunities',
              'Collaborate with sales, product, and support teams',
              'Monitor customer health metrics and proactively address issues'
            ],
            requirements: [
              '3+ years of experience in customer success or account management',
              'Strong interpersonal and relationship-building skills',
              'Experience with CRM systems and customer success tools',
              'Excellent problem-solving and communication abilities',
              'Ability to understand technical concepts and explain them to non-technical users',
              'Bachelor's degree in Business, Marketing, or related field'
            ],
            niceToHave: [
              'Experience in the automotive or parts distribution industry',
              'Knowledge of B2B SaaS platforms',
              'Background in technical support or implementation',
              'Certification in customer success management'
            ],
            postedDate: '2023-02-25',
            isRemote: true
          }
        ];
      } catch (error) {
        console.error('Error fetching job postings:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Scroll to job openings section
    const scrollToJobs = () => {
      const element = document.getElementById('openings');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    };
    
    // Open image gallery
    const openGallery = (index: number) => {
      galleryIndex.value = index;
      galleryDialog.value = true;
    };
    
    // Navigate to previous image
    const prevImage = () => {
      if (galleryIndex.value > 0) {
        galleryIndex.value--;
      }
    };
    
    // Navigate to next image
    const nextImage = () => {
      if (galleryIndex.value < cultureImages.value.length - 1) {
        galleryIndex.value++;
      }
    };
    
    // Initialize component
    onMounted(() => {
      fetchJobs();
    });
    
    return {
      loading,
      jobs,
      filteredJobs,
      selectedDepartment,
      departments,
      companyStats,
      benefits,
      perks,
      cultureImages,
      testimonials,
      galleryDialog,
      galleryIndex,
      selectedImage,
      fetchJobs,
      scrollToJobs,
      openGallery,
      prevImage,
      nextImage
    };
  }
});
</script>

<style scoped>
.culture-card {
  cursor: pointer;
  transition: transform 0.3s;
  overflow: hidden;
}

.hover-zoom:hover {
  transform: scale(1.03);
}
</style>
