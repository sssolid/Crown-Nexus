<!-- frontend/src/views/AboutPage.vue -->
<template>
  <div class="about-page">
    <!-- Hero Section -->
    <section class="about-hero">
      <v-parallax
        src="https://images.unsplash.com/photo-1486262322291-6f1660445269?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
        :height="400"
      >
        <div class="hero-overlay"></div>
        <v-container class="hero-content" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" md="10" lg="8" class="text-center text-white">
              <h1 class="text-h2 font-weight-bold mb-4">About Crown Nexus</h1>
              <h2 class="text-h5 mb-6">Revolutionizing the Automotive Aftermarket Industry Since 2005</h2>
            </v-col>
          </v-row>
        </v-container>
      </v-parallax>
    </section>

    <!-- Mission Statement Section -->
    <section class="py-12">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8" class="text-center">
            <h2 class="text-h4 font-weight-bold mb-8">Our Mission</h2>
            <v-card class="pa-6 bg-primary mb-6">
              <v-card-text class="text-h5 text-white font-italic">
                "To provide quality aftermarket automotive parts through innovative technology and exceptional service, 
                empowering businesses to exceed their customers' expectations."
              </v-card-text>
            </v-card>
            <p class="text-body-1 mb-4">
              At Crown Nexus, we're dedicated to transforming how automotive parts are sourced and distributed. 
              Our B2B platform connects manufacturers, distributors, and retailers in a seamless ecosystem 
              that prioritizes quality, reliability, and efficiency.
            </p>
            <p class="text-body-1">
              We leverage cutting-edge technology to streamline the supply chain, reduce costs, and 
              deliver an unparalleled selection of premium aftermarket parts to our partners.
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Our Story Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Our Story</h2>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-timeline side="end" line-thickness="4" line-color="primary">
              <v-timeline-item
                v-for="(milestone, i) in milestones"
                :key="i"
                :dot-color="milestone.color || 'primary'"
                size="large"
              >
                <template v-slot:opposite>
                  <div class="text-h6 font-weight-bold mb-1">{{ milestone.year }}</div>
                </template>
                <v-card>
                  <v-card-title class="text-h6">{{ milestone.title }}</v-card-title>
                  <v-card-text>{{ milestone.description }}</v-card-text>
                  <v-img
                    v-if="milestone.image"
                    :src="milestone.image"
                    height="200"
                    cover
                    class="rounded-b"
                  ></v-img>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Company Values Section -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Our Values</h2>
            <p class="text-subtitle-1">The principles that drive everything we do</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(value, i) in companyValues" :key="i" cols="12" md="6" lg="4">
            <v-card height="100%" class="d-flex flex-column">
              <v-card-item>
                <template v-slot:prepend>
                  <v-avatar :color="value.color" size="48" class="me-4">
                    <v-icon size="24" :icon="value.icon" color="white"></v-icon>
                  </v-avatar>
                </template>
                <v-card-title class="text-h5">{{ value.title }}</v-card-title>
              </v-card-item>
              <v-card-text class="text-body-1 flex-grow-1">
                {{ value.description }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Leadership Team Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Leadership Team</h2>
            <p class="text-subtitle-1">Meet the experts behind Crown Nexus</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(member, i) in leadershipTeam" :key="i" cols="12" sm="6" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                height="100%"
                class="d-flex flex-column align-center text-center pa-4"
              >
                <v-avatar size="150" class="mb-4">
                  <v-img :src="member.photo" cover></v-img>
                </v-avatar>
                <v-card-title class="text-h5 font-weight-bold">{{ member.name }}</v-card-title>
                <v-card-subtitle class="mb-3">{{ member.title }}</v-card-subtitle>
                <v-card-text class="text-body-2">
                  {{ member.bio }}
                </v-card-text>
                <v-card-actions class="mt-2">
                  <v-btn v-if="member.linkedin" icon variant="text" color="primary" :href="member.linkedin" target="_blank">
                    <v-icon>mdi-linkedin</v-icon>
                  </v-btn>
                  <v-btn v-if="member.twitter" icon variant="text" color="primary" :href="member.twitter" target="_blank">
                    <v-icon>mdi-twitter</v-icon>
                  </v-btn>
                  <v-btn v-if="member.email" icon variant="text" color="primary" :href="`mailto:${member.email}`">
                    <v-icon>mdi-email</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Facilities Section -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" md="6">
            <h2 class="text-h4 font-weight-bold mb-4">Our Facilities</h2>
            <p class="text-body-1 mb-4">
              Crown Nexus operates state-of-the-art distribution centers strategically located 
              across North America to ensure fast, efficient delivery to our partners.
            </p>
            <p class="text-body-1 mb-4">
              Our headquarters in Detroit, Michigan houses our corporate offices, technology center, 
              and main distribution facility - a 250,000 square foot operation equipped with the latest 
              in inventory management and logistics technology.
            </p>
            <p class="text-body-1 mb-6">
              With additional distribution centers in Los Angeles, Dallas, and Atlanta, we provide 
              nationwide coverage with industry-leading shipping times and reliability.
            </p>
            
            <v-list>
              <v-list-subheader class="text-h6 font-weight-bold">By the Numbers</v-list-subheader>
              <v-list-item v-for="(stat, i) in facilityStats" :key="i">
                <template v-slot:prepend>
                  <v-avatar :color="stat.color" size="42">
                    <v-icon :icon="stat.icon" color="white"></v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-h6 font-weight-medium">{{ stat.value }}</v-list-item-title>
                <v-list-item-subtitle>{{ stat.label }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          
          <v-col cols="12" md="6">
            <v-card elevation="0" class="rounded-xl overflow-hidden">
              <v-carousel
                height="500"
                hide-delimiters
                show-arrows="hover"
              >
                <v-carousel-item v-for="(image, i) in facilityImages" :key="i">
                  <v-img :src="image.src" :alt="image.alt" height="500" cover></v-img>
                </v-carousel-item>
              </v-carousel>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Partner Logos Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Our Partners & Certifications</h2>
            <p class="text-subtitle-1">Trusted by industry leaders and certified for quality</p>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12">
            <v-sheet class="d-flex flex-wrap align-center justify-center">
              <v-img
                v-for="(partner, i) in partners"
                :key="i"
                :src="partner.logo"
                :alt="partner.name"
                max-width="180"
                max-height="100"
                contain
                class="ma-4 partner-logo"
              ></v-img>
            </v-sheet>
          </v-col>
        </v-row>

        <v-row class="mt-8">
          <v-col cols="12" class="text-center">
            <v-chip
              v-for="(cert, i) in certifications"
              :key="i"
              color="primary"
              variant="outlined"
              size="large"
              class="ma-2 pa-4"
            >
              <v-icon start :icon="cert.icon" class="me-2"></v-icon>
              {{ cert.name }}
            </v-chip>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Contact CTA Section -->
    <section class="py-12 bg-primary">
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" md="8" lg="6" class="text-center text-white">
            <h2 class="text-h4 font-weight-bold mb-4">Want to learn more?</h2>
            <p class="text-body-1 mb-6">
              Our team is ready to answer your questions and show you how Crown Nexus can transform your parts business.
            </p>
            <v-btn
              color="white"
              size="large"
              variant="elevated"
              class="mx-2"
              to="/contact"
            >
              Contact Us
              <v-icon end icon="mdi-arrow-right"></v-icon>
            </v-btn>
            <v-btn
              color="white"
              size="large"
              variant="outlined"
              class="text-white mx-2"
              to="/demo"
            >
              Request a Demo
              <v-icon end icon="mdi-presentation"></v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

interface Milestone {
  year: string;
  title: string;
  description: string;
  image?: string;
  color?: string;
}

interface CompanyValue {
  title: string;
  description: string;
  icon: string;
  color: string;
}

interface TeamMember {
  name: string;
  title: string;
  bio: string;
  photo: string;
  linkedin?: string;
  twitter?: string;
  email?: string;
}

interface FacilityStat {
  icon: string;
  value: string;
  label: string;
  color: string;
}

interface FacilityImage {
  src: string;
  alt: string;
}

interface Partner {
  name: string;
  logo: string;
}

interface Certification {
  name: string;
  icon: string;
}

export default defineComponent({
  name: 'AboutPage',

  setup() {
    // Company milestones data
    const milestones = ref<Milestone[]>([
      {
        year: '2005',
        title: 'Founding of Crown Nexus',
        description: 'Founded by automotive industry veterans Michael Reynolds and Sarah Chen, Crown Nexus began as a small-scale distributor of specialty brake components.',
        image: 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        color: 'primary'
      },
      {
        year: '2008',
        title: 'Expansion into Full-Line Distribution',
        description: 'Following early success, Crown Nexus expanded its catalog to include a comprehensive range of automotive aftermarket parts and opened its first major distribution center.',
        color: 'info'
      },
      {
        year: '2012',
        title: 'Launch of First Digital Catalog',
        description: 'Crown Nexus revolutionized the industry with the launch of its digital catalog system, allowing customers to search and order parts online for the first time.',
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
      },
      {
        year: '2015',
        title: 'Introduction of CrownFit™ Technology',
        description: 'Our proprietary fitment database technology was launched, providing unprecedented accuracy in part compatibility matching.',
        color: 'success'
      },
      {
        year: '2018',
        title: 'National Expansion',
        description: 'Opened distribution centers in Los Angeles, Dallas, and Atlanta, achieving coast-to-coast coverage and next-day delivery to 85% of the US market.',
        image: 'https://images.unsplash.com/photo-1577416412292-129af7a4c111?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
      },
      {
        year: '2021',
        title: 'Launch of Crown Nexus B2B Platform',
        description: 'Introduced our state-of-the-art B2B platform, integrating inventory management, ordering, and analytics into a seamless digital experience.',
        color: 'warning'
      },
      {
        year: 'Today',
        title: 'Industry Leader',
        description: 'Today, Crown Nexus serves over 5,000 businesses across North America with more than 10,000 quality aftermarket parts, setting the standard for the industry.',
        color: 'error'
      }
    ]);

    // Company values data
    const companyValues = ref<CompanyValue[]>([
      {
        title: 'Quality',
        description: 'We are committed to providing aftermarket parts that meet or exceed OEM specifications, ensuring reliability and customer satisfaction.',
        icon: 'mdi-check-decagram',
        color: 'primary'
      },
      {
        title: 'Innovation',
        description: 'We continuously invest in new technologies and processes to improve our products, services, and the overall customer experience.',
        icon: 'mdi-lightbulb',
        color: 'info'
      },
      {
        title: 'Integrity',
        description: 'We conduct business with honesty, transparency, and ethical standards that build trust with our customers, suppliers, and employees.',
        icon: 'mdi-handshake',
        color: 'success'
      },
      {
        title: 'Partnership',
        description: 'We view our relationships with customers as true partnerships, focusing on mutual growth and long-term success.',
        icon: 'mdi-account-group',
        color: 'error'
      },
      {
        title: 'Expertise',
        description: 'We pride ourselves on deep automotive industry knowledge and product expertise, providing valuable insights to our partners.',
        icon: 'mdi-brain',
        color: 'warning'
      },
      {
        title: 'Reliability',
        description: 'We deliver on our promises with consistent product quality, on-time shipping, and dependable support when our partners need it most.',
        icon: 'mdi-shield-check',
        color: 'secondary'
      }
    ]);

    // Leadership team data
    const leadershipTeam = ref<TeamMember[]>([
      {
        name: 'Michael Reynolds',
        title: 'CEO & Co-Founder',
        bio: 'With over 25 years in the automotive industry, Michael brings extensive experience from both OEM and aftermarket sectors. Prior to founding Crown Nexus, he held executive positions at major auto parts manufacturers.',
        photo: 'https://randomuser.me/api/portraits/men/32.jpg',
        linkedin: '#',
        twitter: '#',
        email: 'michael.reynolds@crownnexus.com'
      },
      {
        name: 'Sarah Chen',
        title: 'COO & Co-Founder',
        bio: 'Sarah's background in supply chain optimization and logistics has been instrumental in building Crown Nexus's efficient distribution network. She holds an MBA from MIT and previously led operations at a Fortune 500 automotive company.',
        photo: 'https://randomuser.me/api/portraits/women/44.jpg',
        linkedin: '#',
        email: 'sarah.chen@crownnexus.com'
      },
      {
        name: 'David Miller',
        title: 'CTO',
        bio: 'David leads our technology initiatives, including the development of our proprietary B2B platform. With a background in software engineering and 15 years in e-commerce, he's transforming how partners interact with our catalog.',
        photo: 'https://randomuser.me/api/portraits/men/67.jpg',
        linkedin: '#',
        twitter: '#'
      },
      {
        name: 'Jennifer Lopez',
        title: 'VP of Product Management',
        bio: 'Jennifer oversees our product catalog strategy and category expansion. Her automotive engineering background and aftermarket expertise ensure we offer the right products to meet market demands.',
        photo: 'https://randomuser.me/api/portraits/women/68.jpg',
        linkedin: '#',
        email: 'jennifer.lopez@crownnexus.com'
      },
      {
        name: 'Robert Washington',
        title: 'VP of Sales',
        bio: 'Robert leads our national sales team with a focus on building strong B2B relationships. His consultative approach has helped hundreds of businesses optimize their parts programs.',
        photo: 'https://randomuser.me/api/portraits/men/91.jpg',
        linkedin: '#',
        twitter: '#'
      },
      {
        name: 'Maria Garcia',
        title: 'VP of Customer Success',
        bio: 'Maria ensures our partners receive exceptional support throughout their journey with Crown Nexus. Her team provides training, technical assistance, and ongoing consultation for continuous improvement.',
        photo: 'https://randomuser.me/api/portraits/women/89.jpg',
        linkedin: '#',
        email: 'maria.garcia@crownnexus.com'
      }
    ]);

    // Facility stats data
    const facilityStats = ref<FacilityStat[]>([
      {
        icon: 'mdi-warehouse',
        value: '4',
        label: 'Distribution Centers',
        color: 'primary'
      },
      {
        icon: 'mdi-package-variant-closed',
        value: '250,000+',
        label: 'Parts in Stock',
        color: 'success'
      },
      {
        icon: 'mdi-truck-fast',
        value: '98.7%',
        label: 'On-Time Delivery Rate',
        color: 'info'
      },
      {
        icon: 'mdi-clock-outline',
        value: '24-48 hrs',
        label: 'Average Order Fulfillment Time',
        color: 'warning'
      }
    ]);

    // Facility images data
    const facilityImages = ref<FacilityImage[]>([
      {
        src: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        alt: 'Crown Nexus Headquarters'
      },
      {
        src: 'https://images.unsplash.com/photo-1553413077-190dd305871c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        alt: 'Distribution Center Interior'
      },
      {
        src: 'https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        alt: 'Automated Warehouse System'
      },
      {
        src: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        alt: 'Technology Center'
      }
    ]);

    // Partners data
    const partners = ref<Partner[]>([
      { name: 'AutoZone', logo: 'https://logo.clearbit.com/autozone.com' },
      { name: 'O\'Reilly Auto Parts', logo: 'https://logo.clearbit.com/oreillyauto.com' },
      { name: 'Advance Auto Parts', logo: 'https://logo.clearbit.com/advanceautoparts.com' },
      { name: 'NAPA Auto Parts', logo: 'https://logo.clearbit.com/napaonline.com' },
      { name: 'CarParts.com', logo: 'https://logo.clearbit.com/carparts.com' },
      { name: 'Summit Racing', logo: 'https://logo.clearbit.com/summitracing.com' },
      { name: 'RockAuto', logo: 'https://logo.clearbit.com/rockauto.com' },
      { name: 'Keystone Automotive', logo: 'https://logo.clearbit.com/keystoneautomotive.com' }
    ]);

    // Certifications data
    const certifications = ref<Certification[]>([
      { name: 'ISO 9001:2015 Certified', icon: 'mdi-certificate' },
      { name: 'AASA Member', icon: 'mdi-car' },
      { name: 'SEMA Member', icon: 'mdi-car-cog' },
      { name: 'AAPEX Verified Supplier', icon: 'mdi-check-decagram' },
      { name: 'AIAG Compliant', icon: 'mdi-shield-check' }
    ]);

    return {
      milestones,
      companyValues,
      leadershipTeam,
      facilityStats,
      facilityImages,
      partners,
      certifications
    };
  }
});
</script>

<style scoped>
.about-hero {
  position: relative;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
}

.hero-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  align-items: center;
}

.on-hover {
  transition: all 0.3s ease;
}

.partner-logo {
  filter: grayscale(100%);
  opacity: 0.7;
  transition: all 0.3s ease;
}

.partner-logo:hover {
  filter: grayscale(0%);
  opacity: 1;
}
</style>
